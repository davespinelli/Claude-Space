#!/usr/bin/env python3
"""Idea 885 (lane C, 2026-09-15) - what makes a RESHAPED length multiset cost +0.0012 in
UNIFORM gaps and nothing in REAL ones?

THE QUANTITY UNDER TEST
-----------------------
Idea 882 ran the 2x2 that un-confounds run LENGTH from run PLACEMENT:

                    | lengths REAL          | lengths reshaped
    ----------------+-----------------------+----------------------------------
    gaps REAL       | OP_REAL == BLOCK      | OP_DOM OP_SPLIT8 OP_LONE OP_FILL
    gaps UNIF (871) | UG_REAL               | SM_DOM SM_SPLIT8 SM_LONE SM_FILL

and put the capped-null residual in NEITHER main effect: the three capped order-preserving
nulls all read inside the calibration band (pure LENGTH channel ~ 0), and UG_REAL read
-0.00003 on clean arms (pure PLACEMENT channel ~ 0).  What is left is the INTERACTION

    I_UNIF(X) = signed(SM_X) - signed(OP_X) - signed(UG_REAL)

which 882 measured at +0.0012 to +0.0023 with the same sign at all three legal cap rules.
Reshaping run lengths is free when the gaps are the real arm's and costs something when the
gaps are 871's uniform composition.  The queue's suspect: 871 draws the gaps INDEPENDENTLY
of the run lengths, and a real arm does not - a long de-grossing run sits in a particular
kind of neighbourhood.  Break a run's length apart from the gaps on either side of it and
you have built a path the market never produces.

WHAT THIS RUN ADDS: A CONDITIONAL GAP DRAW
------------------------------------------
CG = 871's gap draw, BIT-FOR-BIT THE SAME MULTISET, re-ORDERED so that the association
between a run's length and the gaps beside it reproduces the REAL arm's own association.

    kind_seed(CG*_X) == kind_seed(SM_X)

so CG*_X and SM_X are handed the identical md5 stream and therefore the identical gap
multiset AND the identical reshaped length multiset.  They differ in ONE thing: the
permutation that decides which gap sits next to which run.  The contrast

    dCOUPLE(X) = signed(CG_X) - signed(SM_X)

is therefore a same-draw difference with the marginal noise removed by construction, and
gate G_MARG checks the two multisets are equal element-for-element rather than asserting it.

PARAM 1 (conditioning statistic) - which gap a run's length is coupled to:
    PRE   the gap immediately PRECEDING the run          rho_PRE = spearman(L_i, g_i)
    ADJ   the mean of the gaps on EITHER SIDE of the run rho_ADJ = spearman(L_i, (g_i+g_{i+1})/2)
PARAM 2 (cap rule) - 881/882's, verbatim:  REAL / DOM / SPLIT8 / LONE / FILL.
Nothing else is tuned.  The coupling STRENGTH is not a parameter: it is the real arm's own
rho, mapped through the Gaussian copula identity rho_S = (6/pi) asin(rho_P/2), and for ADJ
divided by the construction's own attenuation constant 0.8165 = (2/4)/sqrt(6/16), which is
derived from the averaging, not fitted.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read; 881/882's band reused)
---------------------------------------------------------------------------------------
    H_RHO    the misspecification is real: the REAL arms carry a joint (length, gap)
             association, |median rho| > 0.10 on at least one statistic.  If this fails the
             queue's suspect is dead on arrival and no closure is possible.
    H_CLOSE  (headline) with conditional gaps the interaction closes: for at least one
             conditioning statistic, max over X in {DOM, SPLIT8, LONE, FILL} of
             |I_CG(X)| <= 0.0010 (BLOCK2's band), where
             I_CG(X) = signed(CG_X) - signed(OP_X) - signed(CG_REAL),
             while I_UNIF is outside the band on >= 2 cap rules at 200 seeds.
    H_GAP    the conditional draw moves the null TOWARDS the order-preserving one:
             |signed(CG_X) - signed(OP_X)| < |signed(SM_X) - signed(OP_X)| for >= 3 of 4 X,
             at the statistic H_CLOSE reads.
    H_JOINT  (construction) CG reproduces the real arm's association on the statistic it is
             built on to within 0.10 of the real median, while SM / UG read |rho| <= 0.05.
    H_COSTINV every matched null's signed gap moves < 0.005 across 0 / 10 / 25 bps.

200 SEEDS.  875's budget arithmetic says the residual (~0.0012, per-arm seed SE ~0.004 at
20 seeds) needs >= 200 seeds to resolve; this run uses exactly 200 and reports the achieved
SE next to every reading.  Construction STATISTICS (run-length ratios, achieved rho, k/m
preservation) are read on the first 20 seeds of the same stream - 23,040 draws per null,
far more than any gate needs - while every Sharpe gap uses all 200.

RULE 8 WALK-FORWARD (required, run whatever the verdict)
    IS = ..2016-12-31, OOS = 2017-01-01.. read once.  (a) the signed gaps and the closure
    are measured on the IS window and read on the OOS window per family.  (b) THE BOOKS: one
    declared IS-only selector - the arm with the highest 2009-2016 Sharpe on each panel - is
    picked and its untouched OOS CAGR / Sharpe / MaxDD reported against RULES v2 (live) OOS
    and SPY OOS, BOTH KEEP paths, plus the unselected 4a / 4b base rate over all arms.

SURVIVORSHIP: U56 and B136 are current-constituent lists.  SMALL is the sub-$2B panel with
every ticker whose max_1d_move >= 1.0 in data/small_meta.csv dropped FIRST, and it holds
CURRENT CONSTITUENTS ONLY, so its CAGRs are the most optimistic numbers here and any 4b
reading on it is an upper bound.  This run's headline is a DIFFERENCE BETWEEN TWO NULLS ON
THE SAME ARM AND THE SAME DRAW, far less exposed to that bias than any level.

PROTOCOL: 10 bps per unit turnover (0 and 25 also reported), next-day fills, no shorting, no
leverage.  Deterministic (md5-seeded), standalone, no network.  Modifies nothing but its own
outputs:  .arms.csv  .excess.csv  .gap.csv  .closure.csv  .joint.csv  .walkforward.csv
          .books.csv  .console.txt
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
SIDES = {"BREADTH": ("LO", "HI"), "VOL20": ("HI", "LO"), "DISP": ("HI", "LO"),
         "CORR": ("HI", "LO")}

CAPS = ["REAL", "DOM", "SPLIT8", "LONE", "FILL"]
CAPX = ["DOM", "SPLIT8", "LONE", "FILL"]          # the four reshaping rules
CONDS = ["PRE", "ADJ"]                            # PARAM 1
SPLIT_J = {"DOM": 1, "SPLIT8": 8}
SM_KINDS = [f"SM_{c}" for c in CAPX]
OP_KINDS = [f"OP_{c}" for c in CAPX]
CG_KINDS = [f"CG{cd}_{c}" for cd in CONDS for c in CAPS]
MATCHED = SM_KINDS + OP_KINDS + CG_KINDS + ["UG_REAL", "OP_REAL"]
KINDS = ["BLOCK", "BLOCK2", "UG_REAL"] + SM_KINDS + OP_KINDS + CG_KINDS
NSEED = 200
NSEED_CON = 20                                     # construction stats read on the first 20
SPLIT = "2017-01-01"
ADJ_ATT = 0.5 / np.sqrt(6.0 / 16.0)                # = 0.8165, derived (see module docstring)

PUB882 = dict(sm_dom=-0.00348, sm_split8=+0.00130, sm_lone=+0.00101, sm_fill=+0.00144,
              ug_real_clean=-0.00003)
CAL_BAR, CAL_Z = 0.0010, 2.0
RHO_BAR, JOINT_BAR, FLAT_BAR = 0.10, 0.10, 0.05


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


STATE_FN = {"BREADTH": state_breadth, "VOL20": state_vol20, "DISP": state_disp,
            "CORR": state_corr}


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
    """OP_REAL is handed BLOCK's OWN seed string (882's G8: it must reproduce BLOCK bit-for-bit).
    Every CG null is handed the seed string of the SM null it re-orders, so the two share the
    gap multiset AND the reshaped length multiset exactly and differ only in the coupling."""
    if kind == "OP_REAL":
        return "BLOCK"
    if kind.startswith("CG"):
        cap = kind.split("_", 1)[1]
        return "UG_REAL" if cap == "REAL" else f"SM_{cap}"
    return kind


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
    """CIRCULAR run decomposition (roll-invariant), 882's, verbatim."""
    f = np.asarray(fire, bool)
    if not f.any() or f.all():
        return np.array([], int), np.array([], int)
    i0 = int(np.flatnonzero(f & ~np.roll(f, 1))[0])
    fl, gl = runs_of(np.roll(f, -i0))
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
    """871/875/881/882's gap draw, verbatim."""
    gl = rand_composition(n - k - (m - 1), m + 1, rng, 0)
    gl[1:-1] += 1
    return gl


def _even(total, parts):
    base, rem = divmod(total, parts)
    out = np.full(parts, base, int)
    out[:rem] += 1
    return out


def cap_lengths(cap, fl_real, k, m, lstar, rng):
    """PARAM 2.  881/882's constructions, verbatim."""
    if cap == "REAL":
        return np.asarray(fl_real, int)[rng.permutation(m)]
    if cap == "LONE":
        fl = np.empty(m, int)
        fl[0] = lstar
        if m > 1:
            fl[1:] = _even(k - lstar, m - 1)
        return fl[rng.permutation(m)]
    if cap == "FILL":
        fl = np.ones(m, int)
        rem, capv, i = k - m, max(lstar, 1), 0
        while rem > 0 and i < m:
            take = min(capv - 1, rem)
            fl[i] += take
            rem -= take
            i += 1
        if rem > 0:
            fl[:] = _even(k, m)
        return fl[rng.permutation(m)]
    j = min(SPLIT_J[cap], m)
    fl = np.ones(m, int)
    fl[:j] = _even(k - m + j, j)
    return fl[rng.permutation(m)]


# ------------------------------------------------------------------ the conditional gap draw
_A = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
      1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
_B = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
      6.680131188771972e+01, -1.328068155288572e+01]
_C = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
      -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
_D = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
      3.754408661907416e+00]


def ndtri(p):
    """Inverse standard normal CDF (Acklam), vectorized; |err| < 1.2e-9.  numpy has no erfinv
    and scipy is not a dependency of this repo, so the copula's normal scores are computed
    here rather than imported."""
    p = np.asarray(p, float)
    out = np.empty_like(p)
    lo, hi = p < 0.02425, p > 1 - 0.02425
    mid = ~(lo | hi)
    q = np.sqrt(-2 * np.log(np.where(lo, p, 0.5)))
    out = np.where(lo, (((((_C[0] * q + _C[1]) * q + _C[2]) * q + _C[3]) * q + _C[4]) * q + _C[5])
                   / ((((_D[0] * q + _D[1]) * q + _D[2]) * q + _D[3]) * q + 1), 0.0)
    q = np.sqrt(-2 * np.log(np.where(hi, 1 - p, 0.5)))
    out = np.where(hi, -(((((_C[0] * q + _C[1]) * q + _C[2]) * q + _C[3]) * q + _C[4]) * q + _C[5])
                   / ((((_D[0] * q + _D[1]) * q + _D[2]) * q + _D[3]) * q + 1), out)
    q = np.where(mid, p, 0.5) - 0.5
    r = q * q
    out = np.where(mid, (((((_A[0] * r + _A[1]) * r + _A[2]) * r + _A[3]) * r + _A[4]) * r + _A[5])
                   * q / (((((_B[0] * r + _B[1]) * r + _B[2]) * r + _B[3]) * r + _B[4]) * r + 1),
                   out)
    return out


def _ranks(v):
    """Ordinal ranks 0..m-1 with ties broken by position (deterministic)."""
    return np.argsort(np.argsort(np.asarray(v, float), kind="stable"), kind="stable")


def spearman_np(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3:
        return np.nan
    ra, rb = _ranks(a).astype(float), _ranks(b).astype(float)
    sa, sb = ra.std(), rb.std()
    if sa == 0 or sb == 0:
        return np.nan
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


def couple_gaps(gl2, fl2, cond, rho, rng2):
    """Re-ORDER a drawn gap sequence so that (length, neighbouring gap) reproduces `rho`.

    The gap MULTISET is untouched - only the permutation changes - so this isolates the
    coupling 871's draw destroys.  Gaussian copula: normal scores of the reshaped lengths,
    mixed with independent noise at the Pearson correlation the Spearman identity
    rho_S = (6/pi) asin(rho_P / 2) implies.  For ADJ the target is pre-divided by the
    averaging attenuation 0.8165 (derived, not fitted) because the statistic averages two
    slots.  Slot i sits BEFORE run i; slot m is the trailing gap.
    """
    m = len(fl2)
    if m < 3 or not np.isfinite(rho) or abs(rho) < 1e-9:
        return gl2
    s = ndtri((_ranks(fl2) + 0.5) / m)
    rp = 2.0 * np.sin(np.pi * float(np.clip(rho, -1, 1)) / 6.0)
    if cond == "ADJ":
        rp = rp / ADJ_ATT
    rp = float(np.clip(rp, -0.999, 0.999))
    z = rng2.standard_normal(m + 1)
    t = rp * s + np.sqrt(1.0 - rp * rp) * z[:m]
    slot = np.empty(m + 1)
    if cond == "PRE":
        slot[:m] = t
        slot[m] = z[m]                       # trailing gap is uncoupled by construction
    else:
        slot[0] = t[0]
        slot[m] = t[m - 1]
        slot[1:m] = 0.5 * (t[:m - 1] + t[1:])
    gs = np.sort(gl2)
    nz = int((gs == 0).sum())
    out = np.empty(m + 1, int)
    if nz == 0:
        out[np.argsort(slot, kind="stable")] = gs
        return out
    # 871's draw allows a ZERO only in the leading / trailing gap (it adds 1 to every interior
    # gap precisely so that an interior 0 cannot merge two runs and change m).  A free
    # permutation would move such a zero inside and silently break the matched-null property,
    # so the zeros stay on the boundary slots - the lowest-ranked ones, which is where the
    # coupling would put the smallest gaps anyway - and the coupling orders everything else.
    # The MULTISET is untouched either way, which is what G_MARG checks.
    bs = np.array([0, m]) if nz == 2 else np.array([0 if slot[0] <= slot[m] else m])
    keep = np.ones(m + 1, bool)
    keep[bs] = False
    rest = np.flatnonzero(keep)
    out[bs] = 0
    out[rest[np.argsort(slot[rest], kind="stable")]] = gs[nz:]
    return out


def joint_rho(fl, gl, cond):
    """The association this run is about, on the LINEAR geometry 871's draw actually produces:
    m run lengths and m+1 gaps, gap i immediately preceding run i."""
    m = len(fl)
    if m < 3:
        return np.nan
    if cond == "PRE":
        return spearman_np(fl, gl[:m])
    if cond == "POST":                       # diagnostic only - no null is built on it
        return spearman_np(fl, gl[1:])
    return spearman_np(fl, 0.5 * (np.asarray(gl[:m], float) + np.asarray(gl[1:], float)))


def placebo_eff(m_eff, depth, kind, seed, lstar, rho):
    """Rate-matched, information-free twin of the EFFECTIVE multiplier path m_eff.

    BLOCK / BLOCK2  random circular roll of the real path (the record's reference null).
    UG_* / SM_*     871's UNIFORM gap draw + the cap rule's fire lengths (881/882, verbatim).
    OP_*            the real arm's OWN gap sequence in its OWN order + the cap rule's lengths,
                    then the SAME random circular roll BLOCK gets (882).
    CG{PRE,ADJ}_*   SM's draw, re-ordered to restore the real arm's (length, gap) association.
                    `rho` is a dict {"PRE": .., "ADJ": ..} measured on the REAL arm.
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
    gl2 = _gaps_like_switchmatch(n, k, m, rng)   # identical stream for SM_X and CG*_X
    fl2 = cap_lengths(cap, fl, k, m, lstar, rng)
    if kind.startswith("CG"):
        cond = kind[2:kind.index("_")]
        rng2 = np.random.default_rng(seed ^ (0x9E3779B1 if cond == "PRE" else 0x85EBCA77))
        gl2 = couple_gaps(gl2, fl2, cond, rho.get(cond, np.nan), rng2)
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


def row_sharpe(R):
    sd = R.std(axis=1, ddof=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(sd > 0, R.mean(axis=1) * np.sqrt(252) / sd, np.nan)


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
def gates():
    """Synthetic gates, printed before any hypothesis is read."""
    log("\n[0] GATES (printed before any hypothesis is read)")
    rng = np.random.default_rng(0)
    bad_km = bad_max = bad_gap = bad_len = bad_marg = 0
    g8 = 0.0
    achieved = {f: {k: {c: [] for c in CONDS} for k in KINDS + ["OP_REAL"]}
                for f in ("IND", "CPL")}
    real_rho = {f: {c: [] for c in CONDS} for f in ("IND", "CPL")}
    mx = {k: [] for k in MATCHED}
    NT = 300
    for t in range(NT):
        n = 1200
        fire = np.zeros(n, bool)
        p = int(rng.integers(0, 30))
        # HALF the synthetic arms are built INDEPENDENT (871's own world: a run's length says
        # nothing about the gaps beside it) and half COUPLED (a long run is followed by a long
        # gap).  A construction gate that only ever sees rho = 0 cannot tell a working coupling
        # from a broken one, so G_JOINT is read on the coupled half.
        cpl = t >= NT // 2
        fam_s = "CPL" if cpl else "IND"
        while p < n:
            L = int(rng.integers(1, 25))
            fire[p:p + L] = True
            p += L + (int(3 + 2.2 * L + rng.integers(0, 10)) if cpl
                      else int(rng.integers(3, 60)))
        v = np.where(fire, 0.5, 1.0)
        fl_lin, gl_lin = runs_of(fire)
        fl_c, gl_c = circ_decomp(fire)
        k, m = int(fire.sum()), len(fl_c)
        lstar = int(fl_lin.max())
        lstar_c = int(fl_c.max())
        rho = {c: joint_rho(fl_lin, gl_lin, c) for c in CONDS}
        for c in CONDS:
            real_rho[fam_s][c].append(rho[c])
        draws = {}
        for kind in KINDS + ["OP_REAL"]:
            sd_seed = seed_of("G5", t, kind_seed(kind))
            pe = placebo_eff(v, 0.5, kind, sd_seed, lstar, rho)
            draws[kind] = pe
            pf = pe < 1.0
            pfl_l, pgl_l = runs_of(pf)
            for c in CONDS:
                achieved[fam_s][kind][c].append(joint_rho(pfl_l, pgl_l, c))
            if kind not in MATCHED:
                continue
            pfl, pgl = circ_decomp(pf)
            if int(pf.sum()) != k or len(pfl) != m:
                bad_km += 1
                continue
            mx[kind].append(float(pfl.max()) / lstar_c)
            if kind.rsplit("_", 1)[-1] in ("LONE", "FILL") and int(pfl.max()) > lstar_c:
                bad_max += 1
            if kind.startswith("OP_") and sorted(pgl.tolist()) != sorted(gl_c.tolist()):
                bad_gap += 1
            if kind in ("UG_REAL", "OP_REAL") and sorted(pfl.tolist()) != sorted(fl_c.tolist()):
                bad_len += 1
        # G_MARG: CG*_X carries SM_X's gap AND length multisets, element for element
        for cd in CONDS:
            for cap in CAPS:
                a = draws[f"CG{cd}_{cap}"] < 1.0
                b = draws["UG_REAL" if cap == "REAL" else f"SM_{cap}"] < 1.0
                fa, ga = runs_of(a)
                fb, gb = runs_of(b)
                if (sorted(fa.tolist()) != sorted(fb.tolist())
                        or sorted(ga.tolist()) != sorted(gb.tolist())):
                    bad_marg += 1
        g8 = max(g8, float(np.max(np.abs(draws["OP_REAL"] - draws["BLOCK"]))))
    nm = NT * len(MATCHED)
    log(f"  G5a circular k and m preserved by all {len(MATCHED)} matched nulls: {bad_km} "
        f"violations in {nm} synthetic draws  [{'PASS' if bad_km == 0 else 'FAIL'}]")
    log(f"  G5b LONE / FILL (all gap draws) obey the cap (circ max <= L*): {bad_max} violations "
        f" [{'PASS' if bad_max == 0 else 'FAIL'}]")
    log(f"  G5e OP_* reuse the REAL arm's gap multiset: {bad_gap} violations  "
        f"[{'PASS' if bad_gap == 0 else 'FAIL'}]")
    log(f"  G5f UG_REAL / OP_REAL reuse the REAL arm's fire-length multiset: {bad_len} "
        f"violations  [{'PASS' if bad_len == 0 else 'FAIL'}]")
    log(f"  G8 OP_REAL == BLOCK bit-for-bit (882's zero cell)  max|d| {g8:.3e}  bar 0  "
        f"[{'PASS' if g8 == 0.0 else 'FAIL'}]")
    log(f"  G_MARG CG*_X carries SM_X's gap AND length multisets element-for-element: "
        f"{bad_marg} violations in {NT*len(CONDS)*len(CAPS)}  "
        f"[{'PASS' if bad_marg == 0 else 'FAIL'}]")
    log("  synthetic circ max/L* : " + "  ".join(
        f"{k} {float(np.nanmean(v)):.2f}" for k, v in mx.items() if k in
        ["UG_REAL", "SM_DOM", "OP_DOM", "CGPRE_DOM", "CGADJ_DOM", "SM_LONE", "CGPRE_LONE"]))
    log("\n  G_JOINT (synthetic) - achieved spearman(run length, neighbouring gap), mean over")
    log("  150 INDEPENDENT arms and 150 COUPLED arms (gap length ~ 2.2 x the run before it)")
    log(f"  {'null':13s}{'IND rho_PRE':>13s}{'IND rho_ADJ':>13s}{'CPL rho_PRE':>13s}"
        f"{'CPL rho_ADJ':>13s}")
    log(f"  {'REAL ARM':13s}" + "".join(
        f"{np.nanmean(real_rho[f][c]):13.3f}" for f in ("IND", "CPL") for c in CONDS))
    for kind in ["BLOCK", "UG_REAL", "SM_DOM", "SM_LONE", "OP_DOM", "CGPRE_REAL", "CGPRE_DOM",
                 "CGPRE_LONE", "CGADJ_REAL", "CGADJ_DOM", "CGADJ_LONE"]:
        log(f"  {kind:13s}" + "".join(f"{np.nanmean(achieved[f][kind][c]):13.3f}"
                                      for f in ("IND", "CPL") for c in CONDS))
    tgt = {c: float(np.nanmean(real_rho["CPL"][c])) for c in CONDS}
    gj = {c: abs(float(np.nanmean(achieved["CPL"][f"CG{c}_REAL"][c])) - tgt[c]) for c in CONDS}
    fl_ = max(abs(float(np.nanmean(achieved["CPL"][k][c])))
              for k in ["UG_REAL", "SM_DOM", "SM_LONE"] for c in CONDS)
    log(f"  G_JOINT (synthetic, coupled arms): |CG achieved - real| PRE {gj['PRE']:.3f} "
        f"ADJ {gj['ADJ']:.3f} (bar {JOINT_BAR});  871's own draw reads |rho| <= {fl_:.3f} "
        f"(bar {FLAT_BAR})  "
        f"[{'PASS' if max(gj.values()) <= JOINT_BAR and fl_ <= FLAT_BAR else 'FAIL'}]")
    return dict(g8=g8, bad_marg=bad_marg, bad_km=bad_km)


# ==================================================================================== per panel
def run_panel(name, px, arm_filter=None):
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
    RB = {k: np.ascontiguousarray(v.loc[ii].values) for k, v in base.items()}

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
                    fl_r, gl_r = runs_of(fired)
                    nruns = int(len(fl_r))
                    lstar = int(fl_r.max()) if nruns else 0
                    rho = {c: joint_rho(fl_r, gl_r, c) for c in CONDS + ["POST"]}
                    rho_int = {c: (joint_rho(fl_r[1:-1], gl_r[1:-1], c) if nruns > 4 else np.nan)
                               for c in CONDS + ["POST"]}
                    fl_c, _ = circ_decomp(fired)
                    nruns_c = int(len(fl_c))
                    lstar_c = int(fl_c.max()) if nruns_c else 0
                    for g in GROSSES:
                        if arm_filter is not None and not arm_filter(fam, q, w, depth, cad, g):
                            continue
                        real = {c: apply_eff(RB[(g, c)], me, g, c) for c in RUNGS}
                        rr = real[10]
                        c_, s_, d_ = pack(pd.Series(rr, index=ii))
                        h1, h2 = halves(rr)
                        oc, os_, od = pack(pd.Series(rr[oos], index=ii[oos]))
                        rows.append(dict(
                            panel=name, family=fam, state=st_name, side=side, q=q, w=w,
                            depth=depth, cadence=cad, gross=g, rate=float(fired.mean()),
                            nswitch=sw_real, nruns=nruns, max_runlen=lstar,
                            rho_PRE=rho["PRE"], rho_ADJ=rho["ADJ"], rho_POST=rho["POST"],
                            rho_PRE_int=rho_int["PRE"], rho_ADJ_int=rho_int["ADJ"],
                            rho_POST_int=rho_int["POST"],
                            CAGR=c_, Sharpe=s_, MaxDD=d_, H1=h1, H2=h2,
                            IS_Sharpe=fast_sharpe(rr[isw]), OOS_CAGR=oc, OOS_Sharpe=os_,
                            OOS_MaxDD=od))
                        sh_real = {c: fast_sharpe(real[c]) for c in RUNGS}
                        sh_is, sh_oos = fast_sharpe(rr[isw]), fast_sharpe(rr[oos])
                        for kind in KINDS:
                            P = np.empty((NSEED, len(me)))
                            kmok = 0
                            mxr, ach = [], {c: [] for c in CONDS}
                            for sd in range(NSEED):
                                seed = seed_of(name, fam, q, w, depth, cad, g,
                                               kind_seed(kind), sd)
                                P[sd] = placebo_eff(me, depth, kind, seed, lstar, rho)
                                if sd < NSEED_CON:
                                    pf = P[sd] < 1.0
                                    pfl, _ = circ_decomp(pf)
                                    ok = int(pf.sum()) == k_real and len(pfl) == nruns_c
                                    kmok += int(ok)
                                    if len(pfl) and lstar_c:
                                        mxr.append(float(pfl.max()) / lstar_c)
                                        if kind.rsplit("_", 1)[-1] in ("LONE", "FILL") \
                                                and int(pfl.max()) > lstar_c:
                                            maxviol += 1
                                    pfl_l, pgl_l = runs_of(pf)
                                    for c in CONDS:
                                        ach[c].append(joint_rho(pfl_l, pgl_l, c))
                            g2 = max(g2, float(np.abs(P.mean(axis=1) - me.mean()).max()))
                            if kind in MATCHED:
                                km_viol += NSEED_CON - kmok
                            SW = np.abs(np.diff(P, axis=1, prepend=P[:, :1]))
                            acc = {}
                            for c in RUNGS:
                                R = P * RB[(g, c)][None, :] - SW * (g * c / 1e4)
                                acc[c] = sh_real[c] - row_sharpe(R)
                                if c == 10:
                                    acc_is = sh_is - row_sharpe(R[:, isw])
                                    acc_oos = sh_oos - row_sharpe(R[:, oos])
                            exrows.append(dict(
                                panel=name, family=fam, state=st_name, side=side, q=q, w=w,
                                depth=depth, cadence=cad, gross=g, kind=kind,
                                nswitch_real=sw_real, nruns=nruns, max_runlen_real=lstar,
                                max_run_ratio=float(np.nanmean(mxr)) if mxr else np.nan,
                                km_exact=kmok / NSEED_CON,
                                ach_PRE=float(np.nanmean(ach["PRE"])),
                                ach_ADJ=float(np.nanmean(ach["ADJ"])),
                                **{f"excess_{c}bps": float(np.nanmedian(acc[c])) for c in RUNGS},
                                **{f"seedsd_{c}bps": float(np.nanstd(acc[c], ddof=1))
                                   for c in RUNGS},
                                excess_IS=float(np.nanmedian(acc_is)),
                                excess_OOS=float(np.nanmedian(acc_oos))))
            log(f"    {name}: {fam} q/w done  ({time.time() - t0:.0f}s)")
    return pd.DataFrame(rows), pd.DataFrame(exrows), bench, g2, km_viol, maxviol


# ========================================================================================= main
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 885 - what makes a RESHAPED length multiset cost +0.0012 in UNIFORM gaps and")
    log("           nothing in REAL ones?   CONDITIONAL GAP DRAW.   (lane C 2026-09-15)")
    log("=" * 100)
    log(f"# pandas {pd.__version__} numpy {np.__version__}  |  {len(KINDS)} nulls x {NSEED} "
        f"seeds x {len(RUNGS)} rungs   (construction stats on the first {NSEED_CON})")
    log(f"# PARAM 1 conditioning statistic {CONDS}   PARAM 2 cap rule {CAPS}")
    log(f"# ADJ attenuation constant (derived, not fitted): {ADJ_ATT:.4f}")
    log(f"# quantity being explained: 882's interaction, +0.0012 to +0.0023 at three cap rules")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    for n, p in panels.items():
        log(f"  {n}: {p.shape[1]} cols x {len(p)} days  {p.index[0].date()} .. "
            f"{p.index[-1].date()}")
    gates()

    arms, ex, benches = [], [], []
    g2m = 0.0
    kmv = mxv = 0
    for n, p in panels.items():
        a, e, b, g2, km, mv = run_panel(n, p)
        arms.append(a)
        ex.append(e)
        benches.append(b)
        g2m = max(g2m, g2)
        kmv, mxv = kmv + km, mxv + mv
    arms = pd.concat(arms, ignore_index=True)
    ex = pd.concat(ex, ignore_index=True)
    bench = pd.DataFrame(benches).set_index("panel")
    arms.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    ex.to_csv(OUT / f"{STEM}.excess.csv", index=False)
    log(f"\n  arms {len(arms)} rows, excess {len(ex)} rows  ({time.time()-t0:.0f}s)")
    log(f"  G2 rate match  max|mean(placebo) - mean(real)| {g2m:.3e}  bar 1e-12  "
        f"[{'PASS' if g2m < 1e-12 else 'FAIL'}]")
    ncon = len(MATCHED) * len(arms) * NSEED_CON
    log(f"  G5a-CIRCULAR on REAL arms, all matched nulls: {kmv} of {ncon} "
        f"({kmv/max(ncon,1):.3%})  [{'PASS' if kmv == 0 else 'FAIL'}]")
    log(f"  G5b on REAL arms: LONE / FILL circular max run > L*: {mxv}  "
        f"[{'PASS' if mxv == 0 else 'FAIL'}]")
    log("  Both circular gates inherit 882's named cause: 871's uniform gap draw may put BOTH")
    log("  the leading and the trailing gap at 0, circularly merging the first and last runs.")
    log("  It is a property of THE RECORD'S OWN GAP DRAW, not of anything introduced here, and")
    log("  every headline below is re-read on the violation-free (clean) arms.")

    # ---------------------------------------------------------------- gaps vs BLOCK
    key = ["panel", "family", "q", "w", "depth", "cadence", "gross"]
    vals = ([f"excess_{c}bps" for c in RUNGS] + [f"seedsd_{c}bps" for c in RUNGS]
            + ["excess_IS", "excess_OOS", "max_run_ratio", "ach_PRE", "ach_ADJ"])
    piv = ex.pivot_table(index=key, columns="kind", values=vals)
    gap = {}
    for kind in KINDS:
        for c in RUNGS:
            gap[f"{kind}_ex_{c}"] = piv[(f"excess_{c}bps", kind)]
            gap[f"{kind}_sd_{c}"] = piv[(f"seedsd_{c}bps", kind)]
        for f in ("max_run_ratio", "ach_PRE", "ach_ADJ"):
            gap[f"{kind}_{f}"] = piv[(f, kind)]
        gap[f"{kind}_IS"] = piv[("excess_IS", kind)]
        gap[f"{kind}_OOS"] = piv[("excess_OOS", kind)]
    gap = pd.DataFrame(gap, index=piv.index)
    OTHERS = [k for k in KINDS if k != "BLOCK"]
    add = {}
    for kind in OTHERS:
        for c in RUNGS:
            add[f"s_{kind}_{c}"] = gap[f"{kind}_ex_{c}"] - gap[f"BLOCK_ex_{c}"]
        add[f"dIS_{kind}"] = gap[f"{kind}_IS"] - gap["BLOCK_IS"]
        add[f"dOOS_{kind}"] = gap[f"{kind}_OOS"] - gap["BLOCK_OOS"]
    gap = pd.concat([gap, pd.DataFrame(add, index=gap.index)], axis=1).reset_index()
    clean = (ex[ex["kind"].isin(MATCHED)].groupby(key)["km_exact"].min() == 1.0).rename("clean")
    gap = gap.merge(clean.reset_index(), on=key, how="left")
    gap["clean"] = gap["clean"].fillna(False)
    gap = gap.merge(arms[key + ["rho_PRE", "rho_ADJ", "rho_POST", "nruns"]], on=key, how="left")
    gap.to_csv(OUT / f"{STEM}.gap.csv", index=False)
    NARM = len(gap)

    def signed(kind, c=10, sub=None):
        s = (gap if sub is None else sub)[f"s_{kind}_{c}"].dropna()
        med, mean = float(s.median()), float(s.mean())
        se = float(s.std(ddof=1) / np.sqrt(len(s)))
        below = float((s < 0).mean())
        z = (below - 0.5) / np.sqrt(0.25 / len(s))
        return med, mean, se, below, z

    cl = gap[gap["clean"]]

    log("\n" + "=" * 100)
    log("[1] G7 CALIBRATION at 200 seeds - the band every reading below is judged against")
    log("=" * 100)
    b2 = signed("BLOCK2")
    log(f"  BLOCK2 (BLOCK, independent seed stream) signed median {b2[0]:+.5f}  mean {b2[1]:+.5f}"
        f"  (SE {b2[2]:.5f})  share below {b2[3]:.1%}  z {b2[4]:+.2f}")
    g7 = abs(b2[0]) <= CAL_BAR and abs(b2[4]) < CAL_Z
    log(f"  G7 |signed| <= {CAL_BAR} and |z| < {CAL_Z}  [{'PASS' if g7 else 'FAIL'}]")
    log(f"  seed-noise check: median per-arm seed SD at 10 bps, BLOCK {gap['BLOCK_sd_10'].median():.4f}"
        f"  -> SE of a 200-seed median ~ {1.2533*gap['BLOCK_sd_10'].median()/np.sqrt(NSEED):.5f}"
        f"  (at 20 seeds it was ~{1.2533*gap['BLOCK_sd_10'].median()/np.sqrt(20):.5f})")

    log("\n" + "=" * 100)
    log("[2] G3 - 882's FOUR SM NULLS, re-measured at 200 seeds (same md5 stream, 10x the seeds)")
    log("=" * 100)
    log(f"  {'null':11s}{'882 @20':>10s}{'here @200':>11s}{'delta':>9s}{'SE':>9s}{'z':>8s}")
    for k, pub in (("SM_DOM", PUB882["sm_dom"]), ("SM_SPLIT8", PUB882["sm_split8"]),
                   ("SM_LONE", PUB882["sm_lone"]), ("SM_FILL", PUB882["sm_fill"])):
        s = signed(k)
        log(f"  {k:11s}{pub:+10.5f}{s[0]:+11.5f}{s[0]-pub:+9.5f}{s[2]:9.5f}{s[4]:+8.2f}")
    ugc = signed("UG_REAL", sub=cl)
    log(f"  UG_REAL (clean arms) 882 published {PUB882['ug_real_clean']:+.5f}  here "
        f"{ugc[0]:+.5f}  (SE {ugc[2]:.5f}, z {ugc[4]:+.2f})")

    log("\n" + "=" * 100)
    log("[3] H_RHO - do REAL arms carry the joint (length, gap) association at all?")
    log("=" * 100)
    for c in CONDS + ["POST"]:
        v = arms[f"rho_{c}"].dropna()
        vi = arms[f"rho_{c}_int"].dropna()
        log(f"  rho_{c}: median {v.median():+.3f}  mean {v.mean():+.3f}  IQR "
            f"[{v.quantile(.25):+.3f}, {v.quantile(.75):+.3f}]  share>0 {(v>0).mean():.1%}  "
            f"n {len(v)}")
        log(f"           interior gaps only: median {vi.median():+.3f}  share>0 "
            f"{(vi>0).mean():.1%}")
        log(f"           DIAGNOSTIC (not the pre-registered bar, which is on the SIGNED median):"
            f" median |rho| {v.abs().median():.3f}  share |rho| > 0.20 {(v.abs()>0.20).mean():.1%}")
    for c in CONDS + ["POST"]:
        byp = arms.groupby("panel")[f"rho_{c}"].median()
        log(f"  rho_{c} by panel: " + "  ".join(f"{p} {byp.get(p, np.nan):+.3f}"
                                                for p in ["U56", "B136", "SMALL"]))
        byf = arms.groupby("family")[f"rho_{c}"].median()
        log(f"  rho_{c} by family: " + "  ".join(f"{f} {byf[f]:+.3f}" for f in byf.index))
    rho_med = {c: float(arms[f"rho_{c}"].median()) for c in CONDS + ["POST"]}
    h_rho = max(abs(rho_med[c]) for c in rho_med) > RHO_BAR
    log(f"  H_RHO (|median rho| > {RHO_BAR} on at least one statistic): "
        f"{'CONFIRMED' if h_rho else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[4] G_JOINT on REAL arms - does each null reproduce the real association?")
    log("=" * 100)
    log(f"  {'null':13s}{'ach rho_PRE':>13s}{'ach rho_ADJ':>13s}   (real arms "
        f"{rho_med['PRE']:+.3f} / {rho_med['ADJ']:+.3f})")
    for kind in ["BLOCK", "UG_REAL"] + SM_KINDS + OP_KINDS + CG_KINDS:
        log(f"  {kind:13s}{gap[f'{kind}_ach_PRE'].median():13.3f}"
            f"{gap[f'{kind}_ach_ADJ'].median():13.3f}")
    jt = {}
    for cd in CONDS:
        d_cg = max(abs(float(gap[f"CG{cd}_{cap}_ach_{cd}"].median()) - rho_med[cd])
                   for cap in CAPS)
        d_real = abs(float(gap[f"CG{cd}_REAL_ach_{cd}"].median()) - rho_med[cd])
        flat = max(abs(float(gap[f"{k}_ach_{cd}"].median()))
                   for k in ["UG_REAL"] + SM_KINDS)
        jt[cd] = (d_cg, flat)
        log(f"  CG{cd}: worst |achieved - real| over the 5 cap rules {d_cg:.3f} (bar {JOINT_BAR})"
            f"   at the REAL cap alone {d_real:.3f}   |UG/SM achieved| {flat:.3f} "
            f"(bar {FLAT_BAR})")
    h_joint = any(v[0] <= JOINT_BAR and v[1] <= FLAT_BAR for v in jt.values())
    log(f"  H_JOINT: {'CONFIRMED' if h_joint else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[5] THE INTERACTION - 882's with uniform gaps, and this run's with conditional gaps")
    log("    I_UNIF(X) = s(SM_X) - s(OP_X) - s(UG_REAL)")
    log("    I_CG(X)   = s(CG_X) - s(OP_X) - s(CG_REAL)")
    log("=" * 100)
    clo = []
    for sub_name, sub in (("all arms", gap), ("clean arms", cl)):
        log(f"\n  --- {sub_name} (n={len(sub)}) ---")
        log(f"  {'cap rule':10s}{'I_UNIF':>10s}{'I_CGPRE':>10s}{'I_CGADJ':>10s}"
            f"{'|SM-OP|':>10s}{'|CGPRE-OP|':>12s}{'|CGADJ-OP|':>12s}")
        for X in CAPX:
            iu = float((sub[f"s_SM_{X}_10"] - sub[f"s_OP_{X}_10"]
                        - sub["s_UG_REAL_10"]).median())
            row = dict(subset=sub_name, cap=X, I_UNIF=iu)
            line = f"  {X:10s}{iu:+10.5f}"
            for cd in CONDS:
                ic = float((sub[f"s_CG{cd}_{X}_10"] - sub[f"s_OP_{X}_10"]
                            - sub[f"s_CG{cd}_REAL_10"]).median())
                row[f"I_CG{cd}"] = ic
                line += f"{ic:+10.5f}"
            dsm = abs(float(sub[f"s_SM_{X}_10"].median()) - float(sub[f"s_OP_{X}_10"].median()))
            line += f"{dsm:10.5f}"
            row["d_SM_OP"] = dsm
            for cd in CONDS:
                dcg = abs(float(sub[f"s_CG{cd}_{X}_10"].median())
                          - float(sub[f"s_OP_{X}_10"].median()))
                row[f"d_CG{cd}_OP"] = dcg
                line += f"{dcg:12.5f}"
            log(line)
            clo.append(row)
    clo = pd.DataFrame(clo)
    clo.to_csv(OUT / f"{STEM}.closure.csv", index=False)

    log("\n  the signed gaps themselves (median over all arms, 10 bps, vs BLOCK):")
    log(f"  {'cap rule':10s}{'OP':>10s}{'SM':>10s}{'CGPRE':>10s}{'CGADJ':>10s}"
        f"{'dCOUPLE_PRE':>13s}{'dCOUPLE_ADJ':>13s}")
    for X in CAPS:
        op = f"{signed('OP_'+X)[0]:+10.5f}" if X != "REAL" else f"{0.0:+10.5f}"
        sm = signed("UG_REAL" if X == "REAL" else f"SM_{X}")
        line = f"  {X:10s}{op}{sm[0]:+10.5f}"
        dc = []
        for cd in CONDS:
            cg = signed(f"CG{cd}_{X}")
            line += f"{cg[0]:+10.5f}"
            d = float((gap[f"s_CG{cd}_{X}_10"]
                       - gap[f"s_{'UG_REAL' if X == 'REAL' else 'SM_'+X}_10"]).median())
            dc.append(d)
        log(line + f"{dc[0]:+13.5f}{dc[1]:+13.5f}")

    band = {}
    for cd in CONDS:
        worst = max(abs(float(clo[(clo.subset == "all arms") & (clo.cap == X)]
                              [f"I_CG{cd}"].iloc[0])) for X in CAPX)
        band[cd] = worst
    iu_out = sum(abs(float(clo[(clo.subset == "all arms") & (clo.cap == X)]["I_UNIF"].iloc[0]))
                 > CAL_BAR for X in CAPX)
    h_close = any(v <= CAL_BAR for v in band.values()) and iu_out >= 2
    log(f"\n  worst |I_CG| over the four cap rules: PRE {band['PRE']:.5f}  ADJ {band['ADJ']:.5f}"
        f"   band {CAL_BAR}")
    log(f"  |I_UNIF| outside the band on {iu_out} of 4 cap rules")
    log(f"  H_CLOSE: {'CONFIRMED' if h_close else 'REFUTED'}")
    best_cd = min(CONDS, key=lambda c: band[c])
    n_gap = sum(int(float(clo[(clo.subset == "all arms") & (clo.cap == X)]
                          [f"d_CG{best_cd}_OP"].iloc[0])
                    < float(clo[(clo.subset == "all arms") & (clo.cap == X)]
                            ["d_SM_OP"].iloc[0])) for X in CAPX)
    h_gap = n_gap >= 3
    log(f"  H_GAP (at CG{best_cd}): the conditional draw sits closer to OP than SM does on "
        f"{n_gap} of 4 cap rules: {'CONFIRMED' if h_gap else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[6] EVERY GRID POINT - signed gap at 10 bps by panel, and by (depth, cadence, gross)")
    log("=" * 100)
    show = ["UG_REAL", "CGPRE_REAL", "CGADJ_REAL"] + \
           [k for X in CAPX for k in (f"SM_{X}", f"OP_{X}", f"CGPRE_{X}", f"CGADJ_{X}")] + \
           ["BLOCK2"]
    log(f"  {'null':13s}" + "".join(f"{p:>11s}" for p in ["U56", "B136", "SMALL"])
        + f"{'worst family':>30s}")
    for kind in show:
        byp = gap.groupby("panel")[f"s_{kind}_10"].median()
        byf = gap.groupby("family")[f"s_{kind}_10"].median()
        i = byf.abs().idxmax()
        log(f"  {kind:13s}" + "".join(f"{byp.get(p, np.nan):+11.5f}"
                                      for p in ["U56", "B136", "SMALL"])
            + f"{i + ' ' + format(byf[i], '+.5f'):>30s}")
    log("\n  the INTERACTION at every (depth, cadence, gross) cell, pooled over cap rules:")
    log(f"  {'depth':>7s}{'cad':>5s}{'gross':>7s}{'n':>6s}{'I_UNIF':>10s}{'I_CGPRE':>10s}"
        f"{'I_CGADJ':>10s}")
    cells = []
    for dpt, cad, g in product(DEPTHS, CADENCES, GROSSES):
        sub = gap[(gap.depth == dpt) & (gap.cadence == cad) & (gap.gross == g)]
        if not len(sub):
            continue
        vals3 = []
        for tag in ["UNIF", "CGPRE", "CGADJ"]:
            v = []
            for X in CAPX:
                if tag == "UNIF":
                    v.append(sub[f"s_SM_{X}_10"] - sub[f"s_OP_{X}_10"] - sub["s_UG_REAL_10"])
                else:
                    cd = tag[2:]
                    v.append(sub[f"s_CG{cd}_{X}_10"] - sub[f"s_OP_{X}_10"]
                             - sub[f"s_CG{cd}_REAL_10"])
            vals3.append(float(pd.concat(v).median()))
        cells.append(dict(depth=dpt, cadence=cad, gross=g, n=len(sub), I_UNIF=vals3[0],
                          I_CGPRE=vals3[1], I_CGADJ=vals3[2]))
        log(f"  {dpt:7.2f}{cad:>5s}{g:7.2f}{len(sub):6d}{vals3[0]:+10.5f}{vals3[1]:+10.5f}"
            f"{vals3[2]:+10.5f}")
    pd.DataFrame(cells).to_csv(OUT / f"{STEM}.joint.csv", index=False)

    log("\n" + "=" * 100)
    log("[7] H_COSTINV - the switch counts are matched, so none of this may be a cost story")
    log("=" * 100)
    worst_cost = 0.0
    for kind in OTHERS:
        v = [signed(kind, c)[0] for c in RUNGS]
        rg = max(v) - min(v)
        worst_cost = max(worst_cost, rg)
        log(f"  {kind:13s} signed 0/10/25 = {v[0]:+.5f} / {v[1]:+.5f} / {v[2]:+.5f}   "
            f"range {rg:.5f}")
    h_cost = worst_cost < 0.005
    log(f"  H_COSTINV (worst range {worst_cost:.5f} < 0.005): "
        f"{'CONFIRMED' if h_cost else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[8] RULE 8 (a) - DOES THE CLOSURE WALK FORWARD?  (IS fitted, OOS read once)")
    log("=" * 100)
    wf = []
    for kind in show:
        n_ok = 0
        for fam, g in gap.groupby("family"):
            rho_w = spearman(g[f"dIS_{kind}"], g[f"dOOS_{kind}"])
            wf.append(dict(kind=kind, family=fam, rho=rho_w,
                           IS_median=float(g[f"dIS_{kind}"].median()),
                           OOS_median=float(g[f"dOOS_{kind}"].median())))
            n_ok += int(rho_w >= 0.30)
        log(f"  {kind:13s} rho(IS gap, OOS gap) >= +0.30 in {n_ok} of 8 families")
    wf = pd.DataFrame(wf)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    log("\n  the INTERACTION measured on each window separately (median over arms):")
    log(f"  {'cap rule':10s}{'I_UNIF IS':>12s}{'I_UNIF OOS':>12s}{'I_CGPRE IS':>12s}"
        f"{'I_CGPRE OOS':>13s}{'I_CGADJ IS':>12s}{'I_CGADJ OOS':>13s}")
    for X in CAPX:
        iu_is = float((gap[f"dIS_SM_{X}"] - gap[f"dIS_OP_{X}"] - gap["dIS_UG_REAL"]).median())
        iu_oo = float((gap[f"dOOS_SM_{X}"] - gap[f"dOOS_OP_{X}"] - gap["dOOS_UG_REAL"]).median())
        line = f"  {X:10s}{iu_is:+12.5f}{iu_oo:+12.5f}"
        for cd in CONDS:
            a = float((gap[f"dIS_CG{cd}_{X}"] - gap[f"dIS_OP_{X}"]
                       - gap[f"dIS_CG{cd}_REAL"]).median())
            b = float((gap[f"dOOS_CG{cd}_{X}"] - gap[f"dOOS_OP_{X}"]
                       - gap[f"dOOS_CG{cd}_REAL"]).median())
            line += f"{a:+12.5f}{b:+13.5f}"
        log(line)

    log("\n" + "=" * 100)
    log("[9] RULE 8 (b) - THE BOOKS: IS-only selector, OOS read once, BOTH KEEP PATHS")
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
    log("[10] SUMMARY OF PRE-REGISTERED HYPOTHESES")
    log("=" * 100)
    for nm, v in (("H_RHO", h_rho), ("H_CLOSE", h_close), ("H_GAP", h_gap),
                  ("H_JOINT", h_joint), ("H_COSTINV", h_cost)):
        log(f"  {nm:11s} {'CONFIRMED' if v else 'REFUTED'}")
    log(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

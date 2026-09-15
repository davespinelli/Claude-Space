#!/usr/bin/env python3
"""Idea 905 (lane B, 2026-09-15) - does the PLACEMENT channel (+0.0015) survive a gap draw
that is NOT 871's uniform composition?

THE QUANTITY UNDER TEST
-----------------------
Idea 885 (`2026-09-15_conditional-gap-null-closes-the-INTERACTION_C`) re-measured 882's 2x2
at 200 seeds and found that UG_REAL - the null that keeps the real arm's run LENGTHS
untouched and only redraws WHERE the runs sit, using 871's uniform gap composition - costs

    signed(UG_REAL) = median over 1,152 arms of [ Sharpe(real) - Sharpe(null) ]
                      minus the same quantity for BLOCK
                    = +0.00154 at 10 bps (SE 0.00029), +0.00153 on clean arms

against a BLOCK2 calibration band of -0.00000 (SE 0.00026).  882 had published the same
object as -0.00003 at 20 seeds, i.e. as ZERO.  Reshaping no run at all, merely MOVING the
runs, is the largest legal channel in the whole 2x2.

871's gap draw is a UNIFORM composition: every way of splitting the non-firing days into
m+1 pieces is equally likely.  A real arm's gaps are nothing like that - they are skewed,
they cluster, and a long quiet stretch is followed by another long quiet stretch.  So the
+0.0015 has two possible readings and this run separates them:

    (A) UNIFORMITY.  The channel is a property of the uniform MARGINAL.  Any gap draw that
        respects the arm's own gap distribution costs nothing.
    (B) PLACEMENT.  The channel is a property of REDRAWING placement at all.  Once the gaps
        are re-ordered, it does not matter what they are drawn from.

PARAM 1 (gap draw) - five ways to lay m+1 gaps summing to n-k over the same n days.  All
five are read in 871's own REDUCED space (interior gaps carry a mandatory +1 so two runs
cannot merge; T = n - k - (m-1) is what is actually drawn):

    UNIF    871's uniform composition, VERBATIM (`_gaps_like_switchmatch`).  reference.
    LNFIT   log-normal fitted to the arm's own reduced gaps by moments on log(g+1).
    EBOOT   iid bootstrap of the arm's own reduced-gap multiset (marginal preserved in law).
    GBLOCK  circular BLOCK bootstrap of the arm's own reduced-gap SEQUENCE, block length
            b = round(sqrt(m+1)) - derived from the sample size, not fitted - so local
            serial structure (short gaps clustering with short gaps) partly survives.
    GPERM   a free PERMUTATION of the arm's own reduced-gap multiset.  The marginal is
            preserved EXACTLY, element for element; only the ORDER is destroyed.

GPERM is the decisive level.  It is the one draw whose marginal distance from the real arm
is exactly zero by construction, so:
    GPERM inside the band  -> the channel is a MARGINAL fact (reading A).
    GPERM outside the band -> the channel survives with the marginal held exactly fixed,
                              and it is an ORDER / placement fact (reading B).
Every draw except UNIF is passed through the same largest-remainder projection onto the
exact total T, so the four alternatives differ from each other ONLY in what they draw.

PARAM 2 (cap rule) - 881/882's, verbatim: REAL (no reshaping - the object of the idea),
DOM, LONE.  At REAL the channel is read directly against BLOCK; at DOM and LONE the length
channel is removed by differencing against OP_X (the real arm's OWN gaps in their OWN order
with the same reshaped lengths), so the placement channel is isolated at every cap rule.

Nothing else is tuned.  The block length is derived; the number of seeds is 885's; the arm
grid, the panels, the cost rungs and the md5 seed strings are the record's.

PRE-REGISTERED HYPOTHESES (bars fixed before any number below was read; 885's band reused)
------------------------------------------------------------------------------------------
    H_UNIF   (reading A) at cap REAL, signed(UNIF) > +0.0010 AND every one of LNFIT, EBOOT,
             GBLOCK, GPERM reads |signed| <= 0.0010 (BLOCK2's band).
    H_PLACE  (reading B) at cap REAL all five draws read > +0.0010 with the same sign and
             the spread max - min <= 0.0010.
    H_ORDER  (decisive) signed(GPERM_REAL) > +0.0010 - the channel survives an EXACTLY
             real marginal.
    H_SERIAL |signed(GBLOCK_REAL)| < |signed(GPERM_REAL)| - preserving serial gap structure
             shrinks the channel.
    H_MONO   the channel is a monotone read of how far the draw's marginal sits from the
             real one: spearman(normalised W1 distance, |signed|) >= +0.50 over the 15
             draw x cap cells.
    H_CAPINV the answer does not depend on PARAM 2: for each draw the placement-isolated
             channel carries the same sign at all three cap rules (5 of 5 draws).
    H_COSTINV every kind's signed gap moves < 0.005 across 0 / 10 / 25 bps.

H_UNIF and H_PLACE are mutually exclusive; both may fail, which is the partial answer.

200 SEEDS, the same md5 stream 885 used.  UNIF_REAL is handed UG_REAL's own seed string,
UNIF_DOM SM_DOM's, UNIF_LONE SM_LONE's, so G3 is a BIT-FOR-BIT reproduction of four
committed numbers, not a re-estimate.  Construction statistics (marginal distance, achieved
coupling, k/m preservation) are read on the first 20 seeds; every Sharpe gap uses all 200.

RULE 8 WALK-FORWARD (required, run whatever the verdict)
    IS = ..2016-12-31, OOS = 2017-01-01.. read once.  (a) every signed gap is measured on
    the IS window and read on the OOS window, per family, with rho(IS, OOS).  (b) THE BOOKS:
    one declared IS-only selector - the arm with the highest 2009-2016 Sharpe on each panel
    - is picked and its untouched OOS CAGR / Sharpe / MaxDD reported against RULES v2 (live)
    OOS and SPY OOS, BOTH KEEP paths, plus the unselected 4a / 4b base rate over all arms.

SURVIVORSHIP: U56 and B136 are current-constituent lists.  SMALL is the sub-$2B panel with
every ticker whose max_1d_move >= 1.0 in data/small_meta.csv dropped FIRST, and it holds
CURRENT CONSTITUENTS ONLY, so its CAGRs are the most optimistic numbers here and any 4b
reading on it is an upper bound.  This run's headline is a DIFFERENCE BETWEEN TWO NULLS ON
THE SAME ARM, far less exposed to that bias than any level.

PROTOCOL: 10 bps per unit turnover (0 and 25 also reported), next-day fills, no shorting, no
leverage.  Deterministic (md5-seeded), standalone, no network.  Modifies nothing but its own
outputs:  .arms.csv  .excess.csv  .gap.csv  .draws.csv  .walkforward.csv  .books.csv
          .console.txt
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

DRAWS = ["UNIF", "LNFIT", "EBOOT", "GBLOCK", "GPERM"]      # PARAM 1
CAPS = ["REAL", "DOM", "LONE"]                             # PARAM 2
CAPX = ["DOM", "LONE"]                                     # the reshaping rules
SPLIT_J = {"DOM": 1}
DK = [f"{d}_{c}" for d in DRAWS for c in CAPS]
OP_KINDS = [f"OP_{c}" for c in CAPX]
MATCHED = DK + OP_KINDS
KINDS = ["BLOCK", "BLOCK2"] + DK + OP_KINDS
NSEED = 200
NSEED_CON = 20
SPLIT = "2017-01-01"
CONDS = ["PRE", "ADJ"]

# 885's committed 200-seed readings (same arms, same seeds, same md5 strings) - G3 targets.
PUB885 = {"UNIF_REAL": +0.00154, "UNIF_REAL_clean": +0.00153, "UNIF_DOM": -0.00270,
          "UNIF_LONE": +0.00121, "OP_DOM": -0.00130, "BLOCK2": -0.00000}
PUB885_PANEL = {"UNIF_REAL": {"U56": +0.00136, "B136": +0.00133, "SMALL": +0.00205},
                "OP_LONE": {"U56": -0.00030, "B136": -0.00045, "SMALL": +0.00155}}
PUB885_RUNG = {"UNIF_REAL": {0: +0.00179, 10: +0.00154, 25: +0.00157}}
G3_BAR = 1e-5
CAL_BAR, CAL_Z = 0.0010, 2.0
MONO_BAR = 0.50


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
    """Bit-for-bit continuity with 885/882: the three UNIF kinds are handed the seed strings
    of the committed nulls they ARE (UG_REAL / SM_DOM / SM_LONE), and OP_REAL would be handed
    BLOCK's.  The four new draws get their own independent streams, which is exactly the
    footing BLOCK2 calibrates."""
    return {"UNIF_REAL": "UG_REAL", "UNIF_DOM": "SM_DOM", "UNIF_LONE": "SM_LONE"}.get(kind, kind)


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
    """871/875/881/882/885's gap draw, VERBATIM."""
    gl = rand_composition(n - k - (m - 1), m + 1, rng, 0)
    gl[1:-1] += 1
    return gl


def _even(total, parts):
    base, rem = divmod(total, parts)
    out = np.full(parts, base, int)
    out[:rem] += 1
    return out


def cap_lengths(cap, fl_real, k, m, lstar, rng):
    """PARAM 2.  881/882/885's constructions, VERBATIM (the subset this run uses)."""
    if cap == "REAL":
        return np.asarray(fl_real, int)[rng.permutation(m)]
    if cap == "LONE":
        fl = np.empty(m, int)
        fl[0] = lstar
        if m > 1:
            fl[1:] = _even(k - lstar, m - 1)
        return fl[rng.permutation(m)]
    j = min(SPLIT_J[cap], m)
    fl = np.ones(m, int)
    fl[:j] = _even(k - m + j, j)
    return fl[rng.permutation(m)]


# =================================================================== PARAM 1: the gap draws
def reduce_gaps(gl):
    """871's REDUCED space: strip the mandatory +1 the interior gaps carry, so the object
    drawn is a composition of T = n - k - (m - 1) into m + 1 non-negative parts."""
    g = np.asarray(gl, int).copy()
    if len(g) > 2:
        g[1:-1] -= 1
    return g


def to_composition(raw, T, rng):
    """Project non-negative weights onto the exact integer total T by largest remainder.
    Shape-preserving and deterministic; ties broken by position.  Every alternative draw
    goes through THIS function, so the four alternatives differ only in `raw`."""
    raw = np.asarray(raw, float)
    raw = np.where(np.isfinite(raw) & (raw > 0), raw, 0.0)
    p = len(raw)
    s = raw.sum()
    if T <= 0:
        return np.zeros(p, int)
    if s <= 0:
        return rand_composition(T, p, rng, 0)
    x = raw * (T / s)
    f = np.floor(x).astype(int)
    r = int(T - f.sum())
    if r > 0:
        order = np.argsort(-(x - f), kind="stable")
        f[order[:min(r, p)]] += 1
        r -= min(r, p)
        while r > 0:                                    # only reachable on pathological input
            f[order[:min(r, p)]] += 1
            r -= min(r, p)
    elif r < 0:
        order = np.argsort(x - f, kind="stable")
        for i in order:
            if r == 0:
                break
            take = min(f[i], -r)
            f[i] -= take
            r += take
    return f


def draw_gaps(draw, gred, n, k, m, rng):
    """Return a FULL gap vector (length m+1, sum n-k, interior >= 1) under PARAM 1."""
    if draw == "UNIF":
        return _gaps_like_switchmatch(n, k, m, rng)
    p = m + 1
    T = n - k - (m - 1)
    if draw == "GPERM":
        raw = gred[rng.permutation(p)].astype(float)
    elif draw == "EBOOT":
        raw = gred[rng.integers(0, p, size=p)].astype(float)
    elif draw == "LNFIT":
        y = np.log(gred.astype(float) + 1.0)
        mu, sg = float(y.mean()), float(y.std())
        raw = np.exp(mu + sg * rng.standard_normal(p)) - 1.0
    elif draw == "GBLOCK":
        b = max(1, int(round(np.sqrt(p))))               # derived from p, not fitted
        nb = int(np.ceil(p / b))
        st = rng.integers(0, p, size=nb)
        raw = np.concatenate([gred[(s + np.arange(b)) % p] for s in st])[:p].astype(float)
    else:
        raise ValueError(draw)
    g = to_composition(raw, T, rng)
    if p > 2:
        g[1:-1] += 1
    return g


def placebo_eff(m_eff, depth, kind, seed, lstar):
    """Rate-matched, information-free twin of the EFFECTIVE multiplier path m_eff.

    BLOCK / BLOCK2   random circular roll of the real path (the record's reference null).
    <DRAW>_<CAP>     PARAM 1's gap draw + PARAM 2's fire lengths.  UNIF_* is 871/882/885's
                     construction verbatim and consumes the md5 stream in the same order.
    OP_*             the real arm's OWN gap sequence in its OWN order + the cap rule's
                     lengths, then the SAME random circular roll BLOCK gets (882).
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
    draw, cap = kind.split("_", 1)
    if draw == "OP":
        shift = int(rng.integers(1, n))          # drawn FIRST, so OP_REAL == BLOCK bit-for-bit
        fl2 = cap_lengths(cap, fl, k, m, lstar, rng) if cap != "REAL" else fl
        out = np.ones(n)
        out[assemble(fl2, gl, n)] = 1.0 - depth
        return np.roll(out, shift)
    if (n - k) < (m - 1):                        # infeasible composition; fall back and log
        return np.roll(v, int(rng.integers(1, n)))
    gl2 = draw_gaps(draw, reduce_gaps(gl), n, k, m, rng)   # gaps FIRST (871's stream order)
    fl2 = cap_lengths(cap, fl, k, m, lstar, rng)
    out = np.ones(n)
    out[assemble(fl2, gl2, n)] = 1.0 - depth
    return out


# ---------------------------------------------------------------------------- statistics
def _ranks(v):
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


def joint_rho(fl, gl, cond):
    """885's (length, gap) association on the linear geometry 871's draw produces."""
    m = len(fl)
    if m < 3 or len(gl) < m + 1:
        return np.nan
    if cond == "PRE":
        return spearman_np(fl, gl[:m])
    return spearman_np(fl, 0.5 * (np.asarray(gl[:m], float) + np.asarray(gl[1:m + 1], float)))


def w1(a, b):
    """1-Wasserstein distance between two equal-size samples: mean |sorted diff|."""
    a, b = np.sort(np.asarray(a, float)), np.sort(np.asarray(b, float))
    if len(a) != len(b) or len(a) == 0:
        return np.nan
    return float(np.abs(a - b).mean())


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
    """Synthetic gates on the gap draws themselves, printed before any hypothesis is read."""
    log("\n[0] GATES (printed before any hypothesis is read)")
    rng = np.random.default_rng(0)
    bad_sum = bad_int = bad_km = bad_perm = 0
    g8 = 0.0
    stats = {d: dict(w1=[], cv=[], sh0=[], mx=[]) for d in DRAWS}
    NT = 400
    for t in range(NT):
        n = int(rng.integers(600, 4200))
        # a realistic firing path: a persistent state crossing a threshold (clustered runs)
        z = np.cumsum(rng.standard_normal(n)) * 0.1 + rng.standard_normal(n)
        thr = np.quantile(z, rng.uniform(0.06, 0.30))
        fire = z < thr
        if not (2 <= int(fire.sum()) < n - 2):
            continue
        fl, gl = runs_of(fire)
        m = len(fl)
        k = int(fire.sum())
        if m < 3 or (n - k) < (m - 1):
            continue
        gred = reduce_gaps(gl)
        T = n - k - (m - 1)
        mu_real = float(gred.mean()) if gred.mean() > 0 else 1.0
        me = np.where(fire, 0.5, 1.0)
        for d in DRAWS:
            for s in range(6):
                r2 = np.random.default_rng(seed_of("gate", t, d, s))
                g2 = draw_gaps(d, gred, n, k, m, r2)
                bad_sum += int(g2.sum() != n - k)
                bad_int += int(len(g2) > 2 and (g2[1:-1] < 1).any())
                gr2 = reduce_gaps(g2)
                stats[d]["w1"].append(w1(gr2, gred) / mu_real)
                stats[d]["cv"].append(float(gr2.std() / max(gr2.mean(), 1e-9)))
                stats[d]["sh0"].append(float((gr2 == 0).mean()))
                stats[d]["mx"].append(float(gr2.max()) / max(float(gred.max()), 1.0))
                if d == "GPERM" and not np.array_equal(np.sort(gr2), np.sort(gred)):
                    bad_perm += 1
                pf = assemble(np.asarray(fl, int)[r2.permutation(m)], g2, n)
                bad_km += int(int(pf.sum()) != k or len(runs_of(pf)[0]) != m)
        # G8: OP_REAL must reproduce BLOCK bit-for-bit on the same seed
        sd = seed_of("gate8", t)
        g8 = max(g8, float(np.abs(placebo_eff(me, 0.5, "OP_REAL", sd, int(fl.max()))
                                  - placebo_eff(me, 0.5, "BLOCK", sd, int(fl.max()))).max()))
    log(f"  G4a exact total  (sum gaps == n - k):          {bad_sum} violations  "
        f"[{'PASS' if bad_sum == 0 else 'FAIL'}]")
    log(f"  G4b interior gaps >= 1 (no run merging):       {bad_int} violations  "
        f"[{'PASS' if bad_int == 0 else 'FAIL'}]")
    log(f"  G4c k and m preserved by every draw:           {bad_km} violations  "
        f"[{'PASS' if bad_km == 0 else 'FAIL'}]")
    log(f"  G4d GPERM reduced-gap multiset EXACTLY real:   {bad_perm} violations  "
        f"[{'PASS' if bad_perm == 0 else 'FAIL'}]")
    log(f"  G8  OP_REAL == BLOCK bit-for-bit:              max|d| {g8:.3e}  "
        f"[{'PASS' if g8 == 0.0 else 'FAIL'}]")
    log("\n  what each draw does to the MARGINAL (synthetic clustered arms, reduced gaps):")
    log(f"  {'draw':8s}{'W1/mean':>10s}{'gap CV':>9s}{'share 0':>9s}{'max/real max':>14s}")
    for d in DRAWS:
        s = stats[d]
        log(f"  {d:8s}{np.mean(s['w1']):10.3f}{np.mean(s['cv']):9.3f}{np.mean(s['sh0']):9.3f}"
            f"{np.mean(s['mx']):14.3f}")
    log("  (the real arms' own reduced-gap CV is the GPERM row by construction; a draw whose")
    log("   CV and share-of-zeros sit far from it has changed the marginal, which is exactly")
    log("   the axis H_MONO regresses the channel on.)")
    return dict(bad_sum=bad_sum, bad_int=bad_int, bad_km=bad_km, bad_perm=bad_perm, g8=g8)


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
                    gred_r = reduce_gaps(gl_r)
                    mu_g = float(gred_r.mean()) if len(gred_r) and gred_r.mean() > 0 else 1.0
                    cv_r = float(gred_r.std() / max(gred_r.mean(), 1e-9)) if len(gred_r) else np.nan
                    rho_r = {c: joint_rho(fl_r, gl_r, c) for c in CONDS}
                    fl_c, _ = circ_decomp(fired)
                    nruns_c = int(len(fl_c))
                    lstar_c = int(fl_c.max()) if nruns_c else 0
                    for g in GROSSES:
                        real = {c: apply_eff(RB[(g, c)], me, g, c) for c in RUNGS}
                        rr = real[10]
                        c_, s_, d_ = pack(pd.Series(rr, index=ii))
                        h1, h2 = halves(rr)
                        oc, os_, od = pack(pd.Series(rr[oos], index=ii[oos]))
                        rows.append(dict(
                            panel=name, family=fam, state=st_name, side=side, q=q, w=w,
                            depth=depth, cadence=cad, gross=g, rate=float(fired.mean()),
                            nswitch=sw_real, nruns=nruns, max_runlen=lstar,
                            gap_mean=mu_g, gap_cv=cv_r,
                            rho_PRE=rho_r["PRE"], rho_ADJ=rho_r["ADJ"],
                            CAGR=c_, Sharpe=s_, MaxDD=d_, H1=h1, H2=h2,
                            IS_Sharpe=fast_sharpe(rr[isw]), OOS_CAGR=oc, OOS_Sharpe=os_,
                            OOS_MaxDD=od))
                        sh_real = {c: fast_sharpe(real[c]) for c in RUNGS}
                        sh_is, sh_oos = fast_sharpe(rr[isw]), fast_sharpe(rr[oos])
                        for kind in KINDS:
                            P = np.empty((NSEED, len(me)))
                            kmok = 0
                            wl, cvl, sh0, mxr = [], [], [], []
                            ach = {c: [] for c in CONDS}
                            for sd in range(NSEED):
                                seed = seed_of(name, fam, q, w, depth, cad, g,
                                               kind_seed(kind), sd)
                                P[sd] = placebo_eff(me, depth, kind, seed, lstar)
                                if sd < NSEED_CON:
                                    pf = P[sd] < 1.0
                                    pfl, _ = circ_decomp(pf)
                                    ok = int(pf.sum()) == k_real and len(pfl) == nruns_c
                                    kmok += int(ok)
                                    if len(pfl) and lstar_c:
                                        if kind.rsplit("_", 1)[-1] == "LONE" \
                                                and int(pfl.max()) > lstar_c:
                                            maxviol += 1
                                    pfl_l, pgl_l = runs_of(pf)
                                    gr2 = reduce_gaps(pgl_l)
                                    if len(gr2) == len(gred_r) and len(gr2):
                                        wl.append(w1(gr2, gred_r) / mu_g)
                                    if len(gr2):
                                        cvl.append(float(gr2.std() / max(gr2.mean(), 1e-9)))
                                        sh0.append(float((gr2 == 0).mean()))
                                        mxr.append(float(gr2.max()) / max(float(gred_r.max()), 1.0))
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
                                km_exact=kmok / NSEED_CON,
                                wass=float(np.nanmean(wl)) if wl else np.nan,
                                gap_cv=float(np.nanmean(cvl)) if cvl else np.nan,
                                share0=float(np.nanmean(sh0)) if sh0 else np.nan,
                                max_gap_ratio=float(np.nanmean(mxr)) if mxr else np.nan,
                                ach_PRE=float(np.nanmean(ach["PRE"])),
                                ach_ADJ=float(np.nanmean(ach["ADJ"])),
                                **{f"excess_{c}bps": float(np.nanmedian(acc[c])) for c in RUNGS},
                                **{f"seedsd_{c}bps": float(np.nanstd(acc[c], ddof=1))
                                   for c in RUNGS},
                                excess_IS=float(np.nanmedian(acc_is)),
                                excess_OOS=float(np.nanmedian(acc_oos))))
            log(f"    {name}: {fam} done  ({time.time() - t0:.0f}s)")
    return pd.DataFrame(rows), pd.DataFrame(exrows), bench, g2, km_viol, maxviol


# ========================================================================================= main
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 905 - does the PLACEMENT channel (+0.0015) survive a gap draw that is NOT")
    log("           871's uniform composition?   (lane B 2026-09-15)")
    log("=" * 100)
    log(f"# pandas {pd.__version__} numpy {np.__version__}  |  {len(KINDS)} nulls x {NSEED} "
        f"seeds x {len(RUNGS)} rungs  (construction stats on the first {NSEED_CON})")
    log(f"# PARAM 1 gap draw {DRAWS}   PARAM 2 cap rule {CAPS}")
    log(f"# object being re-priced: 885's signed(UG_REAL) = {PUB885['UNIF_REAL']:+.5f} at 10 bps")
    log("# GBLOCK block length b = round(sqrt(m+1)) is DERIVED from the sample size, not fitted")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    for n, p in panels.items():
        log(f"  {n}: {p.shape[1]} cols x {len(p)} days  {p.index[0].date()} .. "
            f"{p.index[-1].date()}")
    gt = gates()

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
        f"({kmv/max(ncon,1):.3%})")
    log(f"  G5b on REAL arms: LONE circular max run > L*: {mxv}")
    log("  Both circular counts inherit 882/885's named cause: a gap draw may put BOTH the")
    log("  leading and the trailing gap at 0, circularly merging the first and last runs. It")
    log("  is a property of the ENCODING every draw here shares, not of anything new, and")
    log("  every headline below is re-read on the violation-free (clean) arms.")

    # ---------------------------------------------------------------- signed gaps vs BLOCK
    key = ["panel", "family", "q", "w", "depth", "cadence", "gross"]
    vals = ([f"excess_{c}bps" for c in RUNGS] + [f"seedsd_{c}bps" for c in RUNGS]
            + ["excess_IS", "excess_OOS", "wass", "gap_cv", "share0", "max_gap_ratio",
               "ach_PRE", "ach_ADJ"])
    piv = ex.pivot_table(index=key, columns="kind", values=vals)
    gapd = {}
    for kind in KINDS:
        for c in RUNGS:
            gapd[f"{kind}_ex_{c}"] = piv[(f"excess_{c}bps", kind)]
            gapd[f"{kind}_sd_{c}"] = piv[(f"seedsd_{c}bps", kind)]
        for f in ("wass", "gap_cv", "share0", "max_gap_ratio", "ach_PRE", "ach_ADJ"):
            gapd[f"{kind}_{f}"] = piv[(f, kind)]
        gapd[f"{kind}_IS"] = piv[("excess_IS", kind)]
        gapd[f"{kind}_OOS"] = piv[("excess_OOS", kind)]
    gap = pd.DataFrame(gapd, index=piv.index)
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
    gap = gap.merge(arms[key + ["gap_cv", "nruns", "rate"]].rename(
        columns={"gap_cv": "real_gap_cv"}), on=key, how="left")
    gap.to_csv(OUT / f"{STEM}.gap.csv", index=False)

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
    sdm = gap["BLOCK_sd_10"].median()
    log(f"  seed-noise: median per-arm seed SD at 10 bps, BLOCK {sdm:.4f} -> SE of a "
        f"{NSEED}-seed median ~ {1.2533*sdm/np.sqrt(NSEED):.5f}")

    log("\n" + "=" * 100)
    log("[2] G3 - BIT-FOR-BIT REPRODUCTION of 885's committed 200-seed numbers")
    log("    (UNIF_REAL / UNIF_DOM / UNIF_LONE are handed UG_REAL / SM_DOM / SM_LONE's own")
    log("     md5 seed strings, so these must match to floating error, not merely agree)")
    log("=" * 100)
    g3_worst = 0.0
    log(f"  {'quantity':22s}{'885 committed':>15s}{'here':>11s}{'delta':>11s}")
    for k, pub in (("UNIF_REAL", PUB885["UNIF_REAL"]), ("UNIF_DOM", PUB885["UNIF_DOM"]),
                   ("UNIF_LONE", PUB885["UNIF_LONE"]), ("OP_DOM", PUB885["OP_DOM"]),
                   ("BLOCK2", PUB885["BLOCK2"])):
        v = signed(k)[0]
        g3_worst = max(g3_worst, abs(v - pub))
        log(f"  {k:22s}{pub:+15.5f}{v:+11.5f}{v-pub:+11.5f}")
    v = signed("UNIF_REAL", sub=cl)[0]
    g3_worst = max(g3_worst, abs(v - PUB885["UNIF_REAL_clean"]))
    log(f"  {'UNIF_REAL clean arms':22s}{PUB885['UNIF_REAL_clean']:+15.5f}{v:+11.5f}"
        f"{v-PUB885['UNIF_REAL_clean']:+11.5f}")
    for kind, d in PUB885_PANEL.items():
        for p, pub in d.items():
            vv = float(gap[gap.panel == p][f"s_{kind}_10"].median())
            g3_worst = max(g3_worst, abs(vv - pub))
            log(f"  {kind + ' @' + p:22s}{pub:+15.5f}{vv:+11.5f}{vv-pub:+11.5f}")
    for c, pub in PUB885_RUNG["UNIF_REAL"].items():
        vv = signed("UNIF_REAL", c)[0]
        g3_worst = max(g3_worst, abs(vv - pub))
        log(f"  {'UNIF_REAL @' + str(c) + 'bps':22s}{pub:+15.5f}{vv:+11.5f}{vv-pub:+11.5f}")
    log(f"  G3 worst |delta| {g3_worst:.2e}  bar {G3_BAR:.0e} (885 published 5 d.p.)  "
        f"[{'PASS' if g3_worst <= G3_BAR + 5e-6 else 'FAIL'}]")

    log("\n" + "=" * 100)
    log("[3] WHAT EACH DRAW DOES TO THE MARGINAL, on the REAL arms")
    log("=" * 100)
    log(f"  real arms' own reduced-gap CV: median {arms['gap_cv'].median():.3f}  "
        f"IQR [{arms['gap_cv'].quantile(.25):.3f}, {arms['gap_cv'].quantile(.75):.3f}]  "
        f"mean gap {arms['gap_mean'].median():.1f} days")
    log(f"  {'null':12s}{'W1/mean':>10s}{'gap CV':>9s}{'share 0':>9s}{'max/real':>10s}"
        f"{'ach rho_PRE':>13s}{'ach rho_ADJ':>13s}")
    for kind in ["BLOCK"] + DK + OP_KINDS:
        log(f"  {kind:12s}{gap[f'{kind}_wass'].median():10.3f}{gap[f'{kind}_gap_cv'].median():9.3f}"
            f"{gap[f'{kind}_share0'].median():9.3f}{gap[f'{kind}_max_gap_ratio'].median():10.3f}"
            f"{gap[f'{kind}_ach_PRE'].median():13.3f}{gap[f'{kind}_ach_ADJ'].median():13.3f}")
    log("  (W1 is only defined where the null produces the same NUMBER of gaps as the real arm;")
    log("   BLOCK and OP roll the path, so whenever the roll splits a run across the boundary")
    log("   they carry m+1 runs and the cell is undefined - that is why those rows read nan.")
    log("   GPERM's W1 is 0.000 by construction: it permutes the real multiset and changes")
    log("   nothing else, which is what makes it the decisive level.)")

    log("\n" + "=" * 100)
    log("[4] THE HEADLINE - the PLACEMENT channel under five gap draws, cap rule REAL")
    log("    signed(X) = median over arms of [ (Sharpe_real - Sharpe_X) - "
        "(Sharpe_real - Sharpe_BLOCK) ]")
    log("=" * 100)
    log(f"  {'draw':10s}{'signed':>10s}{'mean':>10s}{'SE':>9s}{'mean/SE':>9s}"
        f"{'share<0':>9s}{'z':>8s}{'clean':>10s}")
    head = {}
    for d in DRAWS:
        k = f"{d}_REAL"
        med, mean, se, below, z = signed(k)
        cm = signed(k, sub=cl)[0]
        head[d] = med
        log(f"  {d:10s}{med:+10.5f}{mean:+10.5f}{se:9.5f}{mean/se:+9.2f}{below:9.1%}{z:+8.2f}"
            f"{cm:+10.5f}")
    hdr = []
    for d in DRAWS:
        hdr.append(dict(draw=d, cap="REAL", signed=head[d],
                        wass=float(gap[f"{d}_REAL_wass"].median())))
    h_unif = head["UNIF"] > CAL_BAR and all(abs(head[d]) <= CAL_BAR
                                            for d in DRAWS if d != "UNIF")
    same_sign = len({np.sign(head[d]) for d in DRAWS}) == 1
    spread = max(head.values()) - min(head.values())
    h_place = all(abs(head[d]) > CAL_BAR for d in DRAWS) and same_sign and spread <= CAL_BAR
    h_order = head["GPERM"] > CAL_BAR
    h_serial = abs(head["GBLOCK"]) < abs(head["GPERM"])
    log(f"\n  band {CAL_BAR};  spread max-min {spread:.5f};  all five same sign: {same_sign}")
    log(f"  H_UNIF   (only UNIF outside the band):                    "
        f"{'CONFIRMED' if h_unif else 'REFUTED'}")
    log(f"  H_PLACE  (all five outside, same sign, spread <= {CAL_BAR}):  "
        f"{'CONFIRMED' if h_place else 'REFUTED'}")
    log(f"  H_ORDER  (GPERM - exactly real marginal - outside band):  "
        f"{'CONFIRMED' if h_order else 'REFUTED'}")
    log(f"  H_SERIAL (|GBLOCK| < |GPERM|):                            "
        f"{'CONFIRMED' if h_serial else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[5] PARAM 2 - the same channel at the two RESHAPING cap rules, length channel removed")
    log("    isolated(X, cap) = signed(X_cap) - signed(OP_cap)   [cap REAL: OP_REAL == BLOCK]")
    log("=" * 100)
    log(f"  {'draw':10s}{'REAL':>12s}{'DOM raw':>11s}{'DOM isol':>11s}{'LONE raw':>11s}"
        f"{'LONE isol':>11s}")
    iso = {}
    for d in DRAWS:
        line = f"  {d:10s}{head[d]:+12.5f}"
        iso[d] = {"REAL": head[d]}
        for cap in CAPX:
            raw = signed(f"{d}_{cap}")[0]
            op = signed(f"OP_{cap}")[0]
            iso[d][cap] = raw - op
            line += f"{raw:+11.5f}{raw-op:+11.5f}"
            hdr.append(dict(draw=d, cap=cap, signed=raw, isolated=raw - op,
                            wass=float(gap[f"{d}_{cap}_wass"].median())))
        log(line)
    log(f"  {'OP (anchor)':10s}{0.0:+12.5f}{signed('OP_DOM')[0]:+11.5f}{0.0:+11.5f}"
        f"{signed('OP_LONE')[0]:+11.5f}{0.0:+11.5f}")
    n_capinv = sum(len({np.sign(iso[d][c]) for c in CAPS}) == 1 for d in DRAWS)
    h_capinv = n_capinv == len(DRAWS)
    log(f"\n  H_CAPINV (same sign at all three cap rules): {n_capinv} of {len(DRAWS)} draws  "
        f"{'CONFIRMED' if h_capinv else 'REFUTED'}")
    hdr = pd.DataFrame(hdr)
    hdr.to_csv(OUT / f"{STEM}.draws.csv", index=False)

    log("\n" + "=" * 100)
    log("[6] H_MONO - is the channel a monotone read of MARGINAL DISTANCE?")
    log("=" * 100)
    cells = hdr.copy()
    cells["abs_signed"] = cells.apply(
        lambda r: abs(r["signed"] if r["cap"] == "REAL" else r["isolated"]), axis=1)
    rho_mono = spearman(cells["wass"], cells["abs_signed"])
    h_mono = bool(np.isfinite(rho_mono) and rho_mono >= MONO_BAR)
    log(f"  {'cell':18s}{'W1/mean':>10s}{'|channel|':>12s}")
    for _, r in cells.sort_values("wass").iterrows():
        log(f"  {r['draw'] + '_' + r['cap']:18s}{r['wass']:10.3f}{r['abs_signed']:12.5f}")
    log(f"  spearman(W1, |channel|) over {len(cells)} cells = {rho_mono:+.3f}  "
        f"(bar {MONO_BAR})  H_MONO {'CONFIRMED' if h_mono else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[7] EVERY GRID POINT - signed gap at 10 bps by panel, and by (depth, cadence, gross)")
    log("=" * 100)
    show = [f"{d}_{c}" for c in CAPS for d in DRAWS] + OP_KINDS + ["BLOCK2"]
    log(f"  {'null':13s}" + "".join(f"{p:>11s}" for p in ["U56", "B136", "SMALL"])
        + f"{'worst family':>30s}")
    for kind in show:
        byp = gap.groupby("panel")[f"s_{kind}_10"].median()
        byf = gap.groupby("family")[f"s_{kind}_10"].median()
        i = byf.abs().idxmax()
        log(f"  {kind:13s}" + "".join(f"{byp.get(p, np.nan):+11.5f}"
                                      for p in ["U56", "B136", "SMALL"])
            + f"{i + ' ' + format(byf[i], '+.5f'):>30s}")
    log("\n  cap-REAL channel at every (depth, cadence, gross) cell:")
    log(f"  {'depth':>7s}{'cad':>5s}{'gross':>7s}{'n':>6s}"
        + "".join(f"{d:>11s}" for d in DRAWS))
    grid = []
    for dpt, cad, g in product(DEPTHS, CADENCES, GROSSES):
        sub = gap[(gap.depth == dpt) & (gap.cadence == cad) & (gap.gross == g)]
        if not len(sub):
            continue
        vv = [float(sub[f"s_{d}_REAL_10"].median()) for d in DRAWS]
        grid.append(dict(depth=dpt, cadence=cad, gross=g, n=len(sub),
                         **{d: v for d, v in zip(DRAWS, vv)}))
        log(f"  {dpt:7.2f}{cad:>5s}{g:7.2f}{len(sub):6d}" + "".join(f"{v:+11.5f}" for v in vv))
    log("\n  cap-REAL channel by family (all 8, median over 144 arms each):")
    log(f"  {'family':14s}" + "".join(f"{d:>11s}" for d in DRAWS))
    for fam, sub in gap.groupby("family"):
        log(f"  {fam:14s}" + "".join(f"{float(sub[f's_{d}_REAL_10'].median()):+11.5f}"
                                     for d in DRAWS))
    pd.DataFrame(grid).to_csv(OUT / f"{STEM}.grid.csv", index=False)

    log("\n" + "=" * 100)
    log("[8] H_COSTINV - the switch counts are matched, so none of this may be a cost story")
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
    log("[9] RULE 8 (a) - DOES THE CHANNEL WALK FORWARD?  (IS fitted, OOS read once)")
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
    log("\n  the cap-REAL channel measured on each window separately (median over arms):")
    log(f"  {'draw':10s}{'IS':>12s}{'OOS':>12s}{'OOS - IS':>12s}")
    for d in DRAWS:
        a = float(gap[f"dIS_{d}_REAL"].median())
        b = float(gap[f"dOOS_{d}_REAL"].median())
        log(f"  {d:10s}{a:+12.5f}{b:+12.5f}{b-a:+12.5f}")

    log("\n" + "=" * 100)
    log("[10] RULE 8 (b) - THE BOOKS: IS-only selector, OOS read once, BOTH KEEP PATHS")
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
    log("  NOTE: the arm grid is 885's, so these books are the SAME books 885 committed; the")
    log("  agreement is a gate on this run's plumbing, not a new capital finding.")

    log("\n" + "=" * 100)
    log("[11] SUMMARY OF PRE-REGISTERED HYPOTHESES")
    log("=" * 100)
    for nm, v in (("H_UNIF", h_unif), ("H_PLACE", h_place), ("H_ORDER", h_order),
                  ("H_SERIAL", h_serial), ("H_MONO", h_mono), ("H_CAPINV", h_capinv),
                  ("H_COSTINV", h_cost)):
        log(f"  {nm:11s} {'CONFIRMED' if v else 'REFUTED'}")
    log(f"  gates: G2 {'PASS' if g2m < 1e-12 else 'FAIL'}  "
        f"G3 {'PASS' if g3_worst <= G3_BAR + 5e-6 else 'FAIL'}  "
        f"G4a-d {'PASS' if max(gt['bad_sum'], gt['bad_int'], gt['bad_km'], gt['bad_perm']) == 0 else 'FAIL'}  "
        f"G7 {'PASS' if g7 else 'FAIL'}  G8 {'PASS' if gt['g8'] == 0.0 else 'FAIL'}")
    log(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

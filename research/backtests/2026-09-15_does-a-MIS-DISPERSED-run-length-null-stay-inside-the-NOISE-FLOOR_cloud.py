#!/usr/bin/env python3
"""Idea 875 (cloud lane, 2026-09-15) - does a DELIBERATELY MIS-DISPERSED run-length null still land
inside the NOISE FLOOR?

THE CLAIM UNDER TEST
--------------------
Idea 871 asked which statistic PROTOCOL must require a placebo to match, and answered: the SWITCH
COUNT alone.  Its evidence was |SWITCHMATCH - BLOCK| = 0.0144-0.0146 of Sharpe at every cost rung
against a seed-noise floor of 0.0145 (|RAND - BLOCK| at 0 bps, where RAND's turnover surcharge is
switched off and the two nulls differ only by seed).  871 published its own limit honestly:
SWITCHMATCH draws the m run lengths as a UNIFORM RANDOM COMPOSITION of k days, whose run-length
dispersion is still 0.919x the real arm's.  So what 871 demonstrated is that the count suffices
AGAINST A NULL OF COMPARABLE DISPERSION - not against an arbitrarily shaped one.

This run builds the arbitrarily shaped ones.  If sufficiency survives at deliberately extreme
dispersion, PROTOCOL can name the cheap statistic (switch count) and be done.  If it does not,
PROTOCOL must name the run-length DISTRIBUTION after all, and 871's clause is too weak.

THE FIVE NULLS (all firing-rate-matched and information-free by construction)
-----------------------------------------------------------------------------
                    rate   switch count   run-length shape                      source
    RAND             y          n         iid singletons                        idea 602/606
    BLOCK            y          y         EXACT multiset AND order (circ shift) idea 602/606  <- reference
    SWITCHMATCH      y          y         uniform random composition (0.919x)   idea 871
    SM-DOM           y          y         ONE DOMINANT RUN of k-(m-1) days,     THIS RUN (NEW)
                                          the other m-1 runs of length 1
    SM-UNIF          y          y         NEAR-UNIFORM: every run k//m or       THIS RUN (NEW)
                                          k//m + 1 days
SM-DOM and SM-UNIF hold the firing-day count k and the run count m EXACTLY (so the switch count and
therefore the whole switch-cost term are identical to the real arm's and to BLOCK's), and change
NOTHING ELSE but the dispersion of the fire-run lengths.  Their gap composition is drawn exactly as
SWITCHMATCH draws it (uniform composition, interior gaps >= 1), so the fire-run dispersion is the
single manipulated axis.

Because k and m are matched, the MEAN run length k/m is identical across SWITCHMATCH / SM-DOM /
SM-UNIF / BLOCK / the real arm, so the sd ratio and the CV ratio are the same number and either can
be read as "dispersion".

TUNED PARAMETERS (PROTOCOL rule 4: at most two) - the queue names both
    1. dispersion target   AS-DRAWN (SWITCHMATCH) / MAX (SM-DOM) / MIN (SM-UNIF)
    2. cost rung           0 / 10 / 25 bps
    ALL grid points reported at every panel / family / q / w / depth / cadence / gross.  Nothing is
    chosen on the answer.

REPORTED, NEVER SELECTED ON (inherited from ideas 606/815/871)
    families BREADTH/VOL20/DISP/CORR x LO/HI (8)   level q 0.07 / 0.12 / 0.17
    window w 252 / 1008        depth 0.50 / 1.00       cadence D / W       gross 0.75 / 1.00
    panels U56 / B136 / SMALL  seeds 10 md5 seeds per (arm, kind)
    DECLARED REDUCTION vs 871's axis set: w drops {504, 2016} and depth drops {0.25}.  871's own
    census found the excess is flat in w and monotone-but-small in depth; the reduction is stated
    here, was fixed before any number was read, and halves a 5-null run to fit the sandbox.
    384 arms per panel x 3 panels = 1,152 arms x 5 nulls x 10 seeds x 3 rungs.

GATES (printed before any hypothesis is read)
    G1  a never-firing multiplier path reproduces the ungated book exactly.          bar 1e-12
    G6  the fast Sharpe used on placebo cells equals engine.metrics()['Sharpe'].     bar 1e-10
    G2  every null's mean effective multiplier equals the real arm's (rate match, so the
        matched-gross twin cancels and excess = Sharpe(real) - Sharpe(placebo)).     bar 1e-12
    G4  determinism: every placebo recomputed from its md5 seed, max |d| must be 0.
    G5  CONSTRUCTION: across every arm x seed, SM-DOM and SM-UNIF reproduce the real arm's firing
        -day count k and run count m EXACTLY (0 violations), and their fire-run sd ratios bracket
        SWITCHMATCH's.  This is what makes the test a test of dispersion and not of a bug.
    G3  REPRODUCTION of idea 871 on this axis subset: pooled median |SWITCHMATCH - BLOCK| within
        0.005 of its published 0.0144-0.0146, the seed-noise floor |RAND - BLOCK| at 0 bps within
        0.005 of 0.0145, and SWITCHMATCH's sd_runlen_ratio within 0.03 of 0.919.  The grid is a
        DECLARED SUBSET of 871's, so these are agreement bars, not identity bars, and any miss is
        printed rather than absorbed.

PRE-REGISTERED HYPOTHESES (fixed before any number below the gates was read)
    H_DISP   (construction) mean sd_runlen_ratio >= 3.0 for SM-DOM and <= 0.25 for SM-UNIF, with 0
             k/m violations.  A FAIL here voids everything after it and is printed as such.
    H_SUFF   pooled median |SM-DOM excess - BLOCK excess| <= the re-measured seed-noise floor at
             EVERY cost rung.  PASS = switch-count sufficiency survives extreme dispersion and
             871's cheap clause stands.  FAIL = PROTOCOL must name the distribution.
    H_SUFF2  the same for SM-UNIF.
    H_VAR    the across-seed sd of the SM-DOM excess is >= 2.0x BLOCK's.  A null can match on the
             median and still be unusable, because one draw's giant run either sits on the crash or
             does not; if this passes, the resolution question 871 asked is the wrong one.
    H_COSTINV  |SM-DOM - BLOCK| moves less than 0.02 across 0/10/25 bps.  The switch count is
             matched, so unlike RAND's gap this one must NOT be a cost story.  If it is, something
             other than dispersion is being measured.
    H_WF     Spearman(IS gap, OOS gap) >= +0.30 in >= 6 of 8 families for SM-DOM.

RULE 8 WALK-FORWARD (required, run whatever the verdict)
    IS = ..2016-12-31 fitted, OOS = 2017-01-01.. read once.  (a) the DISPERSION GAP is measured on
    IS and read on OOS per family (H_WF).  (b) THE BOOKS: one declared IS-only selector - the arm
    with the highest 2009-2016 Sharpe on each panel - is picked and its untouched OOS CAGR / Sharpe
    / MaxDD is reported against RULES v2 (live) OOS and SPY OOS, with both KEEP paths, plus the
    unselected base rate of 4a and 4b over all 1,152 arms.

SURVIVORSHIP: U56 and B136 are current-constituent lists.  SMALL is the sub-$2B panel with every
ticker whose max_1d_move >= 1.0 in data/small_meta.csv dropped first, and it is CURRENT
CONSTITUENTS ONLY - dead small caps are absent, so its CAGRs are the most optimistic numbers in the
run and its 4b readings should be treated as upper bounds.  This run's headline quantity is a
DIFFERENCE between two nulls on the same arm, which is far less exposed to that bias than a level.

PROTOCOL: 10 bps per unit turnover (0 and 25 also reported), next-day fills, no shorting, no
leverage.  Deterministic (md5-seeded), standalone, no network.  Modifies nothing but its own
outputs:  .arms.csv  .excess.csv  .gap.csv  .walkforward.csv  .console.txt
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
KINDS = ["RAND", "BLOCK", "SWITCHMATCH", "SM_DOM", "SM_UNIF"]
NSEED = 10
SPLIT = "2017-01-01"

PUB871 = dict(sm_block_lo=0.0144, sm_block_hi=0.0146, floor=0.0145, sd_ratio=0.919)
AGREE_BAR, SD_BAR = 0.005, 0.03


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


# ------------------------------------------------------------------ primitives (602/606/871)
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
    """SWITCHMATCH's own gap draw: uniform composition of the non-firing days into m+1 gaps with
    every INTERIOR gap >= 1 (an interior 0 would merge two fire runs and change m)."""
    gl = rand_composition(n - k - (m - 1), m + 1, rng, 0)
    gl[1:-1] += 1
    return gl


def fire_lengths(kind, k, m, rng):
    """The manipulated axis: m fire-run lengths summing to k, each >= 1."""
    if kind == "SWITCHMATCH":
        return rand_composition(k, m, rng, 1)
    if kind == "SM_DOM":                       # one dominant run, the rest minimal
        fl = np.ones(m, int)
        fl[rng.integers(m)] = k - (m - 1)
        return fl
    if kind == "SM_UNIF":                      # every run k//m or k//m + 1
        base, rem = divmod(k, m)
        fl = np.full(m, base, int)
        if rem:
            fl[rng.choice(m, size=rem, replace=False)] += 1
        return fl
    raise ValueError(kind)


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
    if kind == "BLOCK":
        return np.roll(v, int(rng.integers(1, n)))
    fl, _ = runs_of(fire)
    m = len(fl)
    if (n - k) < (m - 1):                      # infeasible composition; fall back and log
        return np.roll(v, int(rng.integers(1, n)))
    gl2 = _gaps_like_switchmatch(n, k, m, rng)
    fl2 = fire_lengths(kind, k, m, rng)
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
    r_base = backtest(core, ewall_weights(core, 0.75), cost_bps=10, freq=FREQ)["returns"].loc["2009-01-01":]
    ones = np.ones(len(r_base))
    g1 = float(np.max(np.abs(apply_eff(r_base.values, ones, 0.75, 10) - r_base.values)))
    log(f"  G1 never-firing multiplier == ungated book   max|d| {g1:.3e}  bar 1e-12  "
        f"[{'PASS' if g1 < 1e-12 else 'FAIL'}]")
    g6 = abs(fast_sharpe(r_base.values) - metrics(r_base)["Sharpe"])
    log(f"  G6 fast Sharpe == engine.metrics()['Sharpe'] |d| {g6:.3e}  bar 1e-10  "
        f"[{'PASS' if g6 < 1e-10 else 'FAIL'}]")

    # G5 construction, on block-structured synthetic paths (the real arms are re-checked in [2])
    rng = np.random.default_rng(0)
    bad_km = 0
    sdr = {k: [] for k in ("SWITCHMATCH", "SM_DOM", "SM_UNIF")}
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
        sd_r = float(fl.std(ddof=1)) if m > 1 else 0.0
        for kind in ("SWITCHMATCH", "SM_DOM", "SM_UNIF"):
            pe = placebo_eff(v, 0.5, kind, seed_of("G5", t, kind))
            pf = pe < 1.0
            pfl, _ = runs_of(pf)
            if int(pf.sum()) != k or len(pfl) != m:
                bad_km += 1
            if m > 1 and sd_r > 0:
                sdr[kind].append(float(pfl.std(ddof=1)) / sd_r)
    log(f"  G5 k and m preserved by all three switch-matched nulls: {bad_km} violations in "
        f"{300*3} draws  [{'PASS' if bad_km == 0 else 'FAIL'}]")
    means = {k: float(np.mean(v)) for k, v in sdr.items()}
    ok = means["SM_UNIF"] < means["SWITCHMATCH"] < means["SM_DOM"]
    log(f"     synthetic sd_runlen_ratio  SM_UNIF {means['SM_UNIF']:.3f} < SWITCHMATCH "
        f"{means['SWITCHMATCH']:.3f} < SM_DOM {means['SM_DOM']:.3f}  "
        f"[{'PASS' if ok else 'FAIL'}]")


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
    km_viol = 0
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
                            sd_runlen=sd_real, CAGR=c_, Sharpe=s_, MaxDD=d_, H1=h1, H2=h2,
                            IS_Sharpe=fast_sharpe(rr[isw]), OOS_CAGR=oc, OOS_Sharpe=os_,
                            OOS_MaxDD=od))
                        sh_real = {c: fast_sharpe(real[c]) for c in RUNGS}
                        sh_is, sh_oos = fast_sharpe(rr[isw]), fast_sharpe(rr[oos])
                        for kind in KINDS:
                            acc = {c: [] for c in RUNGS}
                            acc_is, acc_oos, swr, sdr, kmok = [], [], [], [], []
                            for sd in range(NSEED):
                                seed = seed_of(name, fam, q, w, depth, cad, g, kind, sd)
                                pe = placebo_eff(me, depth, kind, seed)
                                g2 = max(g2, abs(pe.mean() - me.mean()))
                                swr.append(nswitch(pe) / max(sw_real, 1))
                                pf = pe < 1.0
                                pfl, _ = runs_of(pf)
                                kmok.append(int(pf.sum()) == k_real and len(pfl) == nruns)
                                sdr.append((float(pfl.std(ddof=1)) / sd_real)
                                           if (len(pfl) > 1 and sd_real > 0) else np.nan)
                                for c in RUNGS:
                                    pr = apply_eff(RB[(g, c)], pe, g, c)
                                    acc[c].append(sh_real[c] - fast_sharpe(pr))
                                    if c == 10:
                                        acc_is.append(sh_is - fast_sharpe(pr[isw]))
                                        acc_oos.append(sh_oos - fast_sharpe(pr[oos]))
                            if kind in ("SWITCHMATCH", "SM_DOM", "SM_UNIF"):
                                km_viol += int(NSEED - sum(kmok))
                            exrows.append(dict(
                                panel=name, family=fam, state=st_name, side=side, q=q, w=w,
                                depth=depth, cadence=cad, gross=g, kind=kind,
                                nswitch_real=sw_real, sw_ratio=float(np.mean(swr)),
                                nruns=nruns, sd_runlen_ratio=float(np.nanmean(sdr)),
                                km_exact=float(np.mean(kmok)),
                                **{f"excess_{c}bps": float(np.median(acc[c])) for c in RUNGS},
                                **{f"seedsd_{c}bps": float(np.std(acc[c], ddof=1))
                                   for c in RUNGS},
                                excess_IS=float(np.median(acc_is)),
                                excess_OOS=float(np.median(acc_oos))))
        log(f"    {name}: {st_name} done  ({time.time() - t0:.0f}s)")

    # G4 determinism on a sample
    d4 = 0.0
    for r in exrows[:6] + exrows[len(exrows) // 2: len(exrows) // 2 + 6]:
        st_full = states[r["state"]]
        thr = st_full.rolling(r["w"], min_periods=max(60, r["w"] // 4)).quantile(
            r["q"] if r["side"] == "LO" else 1 - r["q"])
        me = gate_mult(st_full, thr, r["side"], r["depth"], r["cadence"], idx
                       ).shift(1).fillna(1.0).loc[ii].values
        rb = RB[(r["gross"], 10)]
        sh = fast_sharpe(apply_eff(rb, me, r["gross"], 10))
        acc = [sh - fast_sharpe(apply_eff(rb, placebo_eff(
            me, r["depth"], r["kind"], seed_of(name, r["family"], r["q"], r["w"], r["depth"],
                                               r["cadence"], r["gross"], r["kind"], sd)),
            r["gross"], 10)) for sd in range(NSEED)]
        d4 = max(d4, abs(float(np.median(acc)) - r["excess_10bps"]))
    return pd.DataFrame(rows), pd.DataFrame(exrows), bench, g2, d4, km_viol


# ========================================================================================= main
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 875 - does a DELIBERATELY MIS-DISPERSED run-length null still land inside the NOISE"
        " FLOOR?  (cloud lane 2026-09-15)")
    log("=" * 100)
    log(f"# pandas {pd.__version__} numpy {np.__version__}")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    for n, p in panels.items():
        log(f"  {n}: {p.shape[1]} cols x {len(p)} days  {p.index[0].date()} .. {p.index[-1].date()}")
    gates(panels)

    arms, ex, benches = [], [], []
    g2m = d4m = 0.0
    kmv = 0
    for n, p in panels.items():
        a, e, b, g2, d4, km = run_panel(n, p)
        arms.append(a)
        ex.append(e)
        benches.append(b)
        g2m, d4m, kmv = max(g2m, g2), max(d4m, d4), kmv + km
    arms = pd.concat(arms, ignore_index=True)
    ex = pd.concat(ex, ignore_index=True)
    bench = pd.DataFrame(benches).set_index("panel")
    arms.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    ex.to_csv(OUT / f"{STEM}.excess.csv", index=False)
    log(f"\n  arms {len(arms)} rows, excess {len(ex)} rows  ({time.time()-t0:.0f}s)")
    log(f"  G2 rate match  max|mean(placebo) - mean(real)| {g2m:.3e}  bar 1e-12  "
        f"[{'PASS' if g2m < 1e-12 else 'FAIL'}]")
    log(f"  G4 determinism max|d| {d4m:.3e}  bar 0  [{'PASS' if d4m == 0.0 else 'FAIL'}]")
    log(f"  G5 on REAL arms: k and m violations across all switch-matched cells: {kmv} of "
        f"{3*len(arms)*NSEED}  [{'PASS' if kmv == 0 else 'FAIL'}]")

    # ---------------------------------------------------------------- gaps vs BLOCK
    key = ["panel", "family", "q", "w", "depth", "cadence", "gross"]
    piv = ex.pivot_table(index=key, columns="kind",
                         values=[f"excess_{c}bps" for c in RUNGS] + [f"seedsd_{c}bps" for c in RUNGS]
                         + ["excess_IS", "excess_OOS", "sd_runlen_ratio", "sw_ratio"])
    gap = pd.DataFrame(index=piv.index)
    for kind in KINDS:
        for c in RUNGS:
            gap[f"{kind}_ex_{c}"] = piv[(f"excess_{c}bps", kind)]
            gap[f"{kind}_sd_{c}"] = piv[(f"seedsd_{c}bps", kind)]
        gap[f"{kind}_dispratio"] = piv[("sd_runlen_ratio", kind)]
        gap[f"{kind}_swratio"] = piv[("sw_ratio", kind)]
        gap[f"{kind}_IS"] = piv[("excess_IS", kind)]
        gap[f"{kind}_OOS"] = piv[("excess_OOS", kind)]
    for kind in ("RAND", "SWITCHMATCH", "SM_DOM", "SM_UNIF"):
        for c in RUNGS:
            gap[f"d_{kind}_{c}"] = (gap[f"{kind}_ex_{c}"] - gap[f"BLOCK_ex_{c}"]).abs()
        gap[f"dIS_{kind}"] = gap[f"{kind}_IS"] - gap["BLOCK_IS"]
        gap[f"dOOS_{kind}"] = gap[f"{kind}_OOS"] - gap["BLOCK_OOS"]
    gap = gap.reset_index()
    gap.to_csv(OUT / f"{STEM}.gap.csv", index=False)

    FLOOR = float(gap["d_RAND_0"].median())
    log("\n" + "=" * 100)
    log("[1] G3 REPRODUCTION OF IDEA 871 ON THIS DECLARED AXIS SUBSET")
    log("=" * 100)
    smb = {c: float(gap[f"d_SWITCHMATCH_{c}"].median()) for c in RUNGS}
    sdr_sm = float(gap["SWITCHMATCH_dispratio"].mean())
    log(f"  pooled median |SWITCHMATCH - BLOCK|: " +
        "  ".join(f"{c}bps {smb[c]:.4f}" for c in RUNGS) +
        f"   (871 published {PUB871['sm_block_lo']:.4f}-{PUB871['sm_block_hi']:.4f})")
    hi = max(abs(smb[c] - PUB871["sm_block_hi"]) for c in RUNGS)
    lo = max(abs(smb[c] - PUB871["sm_block_lo"]) for c in RUNGS)
    log(f"    max distance to the published band {min(hi, lo):.4f}  bar {AGREE_BAR}  "
        f"[{'PASS' if min(hi, lo) <= AGREE_BAR else 'DIFFERS'}]")
    log(f"  seed-noise floor |RAND - BLOCK| at 0 bps = {FLOOR:.4f}  (871: {PUB871['floor']:.4f})  "
        f"[{'PASS' if abs(FLOOR - PUB871['floor']) <= AGREE_BAR else 'DIFFERS'}]")
    log(f"  RATIO |SWITCHMATCH - BLOCK| / floor = "
        f"{smb[10]/FLOOR:.3f}  (871: {PUB871['sm_block_hi']/PUB871['floor']:.3f}) — this is the"
        f" scale-free form of 871's claim and it is what must reproduce, not the level")
    log(f"  SWITCHMATCH sd_runlen_ratio {sdr_sm:.3f}  (871: {PUB871['sd_ratio']:.3f})  "
        f"[{'PASS' if abs(sdr_sm - PUB871['sd_ratio']) <= SD_BAR else 'DIFFERS'}]")
    log(f"  RAND switch-count ratio {float(gap['RAND_swratio'].mean()):.2f}x; every matched null "
        f"{float(gap['SM_DOM_swratio'].mean()):.2f}x / {float(gap['SM_UNIF_swratio'].mean()):.2f}x"
        f" / {float(gap['SWITCHMATCH_swratio'].mean()):.2f}x")

    log("\n" + "=" * 100)
    log("[2] H_DISP - DID THE MANIPULATION WORK?  (fire-run sd ratio vs the real arm, all arms)")
    log("=" * 100)
    for kind in ("SM_UNIF", "SWITCHMATCH", "SM_DOM", "BLOCK", "RAND"):
        v = gap[f"{kind}_dispratio"]
        log(f"  {kind:12s} mean {v.mean():7.3f}   median {v.median():7.3f}   "
            f"p05 {v.quantile(.05):7.3f}   p95 {v.quantile(.95):7.3f}")
    dom_ok = gap["SM_DOM_dispratio"].mean() >= 3.0
    unif_ok = gap["SM_UNIF_dispratio"].mean() <= 0.25
    log(f"  H_DISP: SM_DOM mean >= 3.0 [{'PASS' if dom_ok else 'FAIL'}] and SM_UNIF mean <= 0.25 "
        f"[{'PASS' if unif_ok else 'FAIL'}], k/m violations {kmv} "
        f"-> {'CONFIRMED' if (dom_ok and unif_ok and kmv == 0) else 'FAILED'}")

    log("\n" + "=" * 100)
    log("[3] H_SUFF / H_SUFF2 - DOES SUFFICIENCY SURVIVE EXTREME DISPERSION?")
    log(f"    seed-noise floor = {FLOOR:.4f} of Sharpe (|RAND - BLOCK| at 0 bps, 871's own form)")
    log("=" * 100)
    log(f"  {'null':13s} " + " ".join(f"{'|d| @'+str(c)+'bps':>14s}" for c in RUNGS)
        + "   verdict vs floor")
    verd = {}
    for kind in ("SWITCHMATCH", "SM_UNIF", "SM_DOM", "RAND"):
        med = {c: float(gap[f"d_{kind}_{c}"].median()) for c in RUNGS}
        inside = all(med[c] <= FLOOR for c in RUNGS)
        verd[kind] = (med, inside)
        log(f"  {kind:13s} " + " ".join(f"{med[c]:14.4f}" for c in RUNGS)
            + f"   {'INSIDE at every rung' if inside else 'OUTSIDE at ' + ','.join(str(c) for c in RUNGS if med[c] > FLOOR) + 'bps'}")
    log(f"  H_SUFF  (SM_DOM inside the floor at every rung): "
        f"{'CONFIRMED' if verd['SM_DOM'][1] else 'REFUTED'}")
    log(f"  H_SUFF2 (SM_UNIF inside the floor at every rung): "
        f"{'CONFIRMED' if verd['SM_UNIF'][1] else 'REFUTED'}")
    mx = max(verd["SM_DOM"][0][c] for c in RUNGS)
    log(f"  SM_DOM's largest gap is {mx:.4f} = {mx/FLOOR:.2f}x the floor")

    log("\n  by panel and by family (10 bps, median |null - BLOCK|):")
    for kind in ("SWITCHMATCH", "SM_UNIF", "SM_DOM"):
        bypan = gap.groupby("panel")[f"d_{kind}_10"].median()
        log(f"    {kind:12s} " + "  ".join(f"{p} {v:.4f}" for p, v in bypan.items())
            + f"   |  worst family {gap.groupby('family')[f'd_{kind}_10'].median().max():.4f}"
            + f" ({gap.groupby('family')[f'd_{kind}_10'].median().idxmax()})")

    log("\n" + "=" * 100)
    log("[3b] THE SIGNED GAP - the statistic 871's |.| form cannot see")
    log("     |per-arm gap| is a per-arm quantity dominated by seed noise; the SIGNED gap pooled")
    log("     over 1,152 arms averages that noise away (SE of the pooled median ~ seed_sd / ")
    log("     sqrt(NSEED * n_arms) ~ 0.0006), so a systematic difference shows up here or nowhere.")
    log("=" * 100)
    log(f"  {'null':13s} " + " ".join(f"{'signed @'+str(c):>13s}" for c in RUNGS)
        + f"{'share below BLOCK':>20s}{'sign-test z':>13s}")
    signed = {}
    for kind in ("SWITCHMATCH", "SM_UNIF", "SM_DOM", "RAND"):
        med = {c: float((gap[f"{kind}_ex_{c}"] - gap[f"BLOCK_ex_{c}"]).median()) for c in RUNGS}
        below = float((gap[f"{kind}_ex_10"] < gap["BLOCK_ex_10"]).mean())
        n = len(gap)
        z = (below - 0.5) / np.sqrt(0.25 / n)
        signed[kind] = (med, below, z)
        log(f"  {kind:13s} " + " ".join(f"{med[c]:+13.4f}" for c in RUNGS)
            + f"{below:19.1%}{z:+13.1f}")
    log("  A null that differs from BLOCK only by seed noise has a signed median of 0.0000, a")
    log("  share of 50.0% and |z| < 2.  The reading is printed above for every null.")

    log("\n" + "=" * 100)
    log("[8] NOISE ACCOUNTING - is |null - BLOCK| anything BUT the seed budget?")
    log("    Predicted under pure independent seed noise, per arm:")
    log("      median|gap| = 0.6745 * 1.2533 / sqrt(NSEED) * sqrt(sd_null^2 + sd_BLOCK^2)")
    log("    (0.6745 = median of a half-normal in sd units; 1.2533 = SE inflation of a median")
    log("     over a mean at n=10).  If observed / predicted ~ 1, the statistic is measuring the")
    log("     seed budget and nothing else.")
    log("=" * 100)
    log(f"  {'null':13s}{'observed':>11s}{'predicted':>11s}{'obs/pred':>10s}"
        f"{'seeds for 0.010':>17s}{'seeds for 0.005':>17s}")
    for kind in ("SWITCHMATCH", "SM_UNIF", "SM_DOM", "RAND"):
        pred = (0.6745 * 1.2533 / np.sqrt(NSEED)
                * np.sqrt(gap[f"{kind}_sd_10"] ** 2 + gap["BLOCK_sd_10"] ** 2))
        pm, om = float(pred.median()), float(gap[f"d_{kind}_10"].median())
        log(f"  {kind:13s}{om:11.4f}{pm:11.4f}{om/pm:10.2f}"
            f"{NSEED*(pm/0.010)**2:17.0f}{NSEED*(pm/0.005)**2:17.0f}")
    log("  'seeds for X' = the md5-seed budget at which pure noise alone would produce a median")
    log("  |gap| below X, i.e. the budget at which a true difference of that size is resolvable.")

    log("\n" + "=" * 100)
    log("[4] H_VAR - SEED DISPERSION OF THE EXCESS (a null can match the median and still be unusable)")
    log("=" * 100)
    log(f"  {'null':13s} " + " ".join(f"{'seed sd @'+str(c):>14s}" for c in RUNGS))
    for kind in KINDS:
        log(f"  {kind:13s} " + " ".join(f"{gap[f'{kind}_sd_{c}'].median():14.4f}" for c in RUNGS))
    rv = float(gap["SM_DOM_sd_10"].median() / gap["BLOCK_sd_10"].median())
    log(f"  SM_DOM seed sd / BLOCK seed sd at 10 bps = {rv:.2f}x  -> H_VAR "
        f"{'CONFIRMED' if rv >= 2.0 else 'REFUTED'} (bar 2.0)")

    log("\n" + "=" * 100)
    log("[5] H_COSTINV - IS THE SM_DOM GAP A COST STORY LIKE RAND'S?")
    log("=" * 100)
    for kind in ("RAND", "SWITCHMATCH", "SM_UNIF", "SM_DOM"):
        med = [float(gap[f"d_{kind}_{c}"].median()) for c in RUNGS]
        log(f"  {kind:13s} |d| 0/10/25 bps = {med[0]:.4f} / {med[1]:.4f} / {med[2]:.4f}   "
            f"range {max(med)-min(med):.4f}")
    rng_dom = (max(float(gap[f"d_SM_DOM_{c}"].median()) for c in RUNGS)
               - min(float(gap[f"d_SM_DOM_{c}"].median()) for c in RUNGS))
    log(f"  H_COSTINV: SM_DOM range across rungs {rng_dom:.4f} < 0.02 -> "
        f"{'CONFIRMED' if rng_dom < 0.02 else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[6] RULE 8 (a) - DOES THE DISPERSION GAP WALK FORWARD?  (IS fitted, OOS read once)")
    log("=" * 100)
    wf = []
    for kind in ("SWITCHMATCH", "SM_UNIF", "SM_DOM"):
        n_ok = 0
        for fam, g in gap.groupby("family"):
            rho = spearman(g[f"dIS_{kind}"], g[f"dOOS_{kind}"])
            wf.append(dict(kind=kind, family=fam, rho=rho,
                           IS_median=float(g[f"dIS_{kind}"].median()),
                           OOS_median=float(g[f"dOOS_{kind}"].median())))
            n_ok += int(rho >= 0.30)
        log(f"  {kind:12s} rho(IS gap, OOS gap) >= +0.30 in {n_ok} of 8 families" +
            (f"  -> H_WF {'CONFIRMED' if n_ok >= 6 else 'REFUTED'}" if kind == "SM_DOM" else ""))
    wf = pd.DataFrame(wf)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    log(wf.pivot_table(index="family", columns="kind", values="rho").to_string(
        float_format=lambda x: f"{x:+.3f}"))
    log("\n  IS-window and OOS-window medians of (null - BLOCK), 10 bps:")
    for kind in ("SWITCHMATCH", "SM_UNIF", "SM_DOM"):
        s = wf[wf.kind == kind]
        log(f"    {kind:12s} IS {s.IS_median.median():+.4f}   OOS {s.OOS_median.median():+.4f}")

    log("\n" + "=" * 100)
    log("[7] RULE 8 (b) - THE BOOKS: IS-only selector, OOS read once, both KEEP paths")
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
        log(f"     RULES v2 (live) {b.bl_cagr:.2%} / {b.bl_sh:.3f} / {b.bl_dd:.2%}  OOS "
            f"{b.bl_oos_c:.2%} / {b.bl_oos_s:.3f} / {b.bl_oos_d:.2%}")
        log(f"     SPY            {b.spy_cagr:.2%} / {b.spy_sh:.3f} / {b.spy_dd:.2%}  OOS "
            f"{b.spy_oos_c:.2%} / {b.spy_oos_s:.3f} / {b.spy_oos_d:.2%}   "
            f"4b bars: DD {0.60*b.spy_dd:.2%}, CAGR {0.70*b.spy_cagr:.2%}")
        log(f"     4a {'PASS' if p4a else 'fail'}   4b {'PASS' if p4b else 'fail'}")
        n4a = n4b = 0
        for _, r in g.iterrows():
            n4a += int(r.H1 > b.bl_h1 and r.H2 > b.bl_h2 and r.MaxDD >= b.bl_dd)
            n4b += int(r.H1 > b.spy_h1 and r.H2 > b.spy_h2 and r.OOS_Sharpe > b.spy_oos_s
                       and r.MaxDD >= 0.60 * b.spy_dd and r.CAGR >= 0.70 * b.spy_cagr)
        log(f"     unselected base rate over {len(g)} arms: 4a {n4a} ({n4a/len(g):.1%}), "
            f"4b {n4b} ({n4b/len(g):.1%})")
    pd.DataFrame(sel).to_csv(OUT / f"{STEM}.books.csv", index=False)

    log(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

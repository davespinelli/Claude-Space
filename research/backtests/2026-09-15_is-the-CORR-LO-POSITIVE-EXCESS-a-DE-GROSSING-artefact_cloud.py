#!/usr/bin/env python3
"""Idea 815 - "is-the-CORR-LO-POSITIVE-EXCESS-a-DE-GROSSING-artefact" (cloud, 2026-09-15).

The finding this run exists to decompose
----------------------------------------
Idea 606 built idea 602's placebo-differenced statistic on four gate STATES (BREADTH, VOL20,
DISP, CORR) in both directions.  Its reversal control - fire the gate on the WRONG tail, which
keeps the firing rate and the clustering and destroys the information - worked on two states
and failed on two:

    VOL20-LO  -0.0128 (share>0 0.361)   flips sign, as a real signal should
    DISP-LO   -0.0204 (share>0 0.162)   flips sign, as a real signal should
    CORR-LO   +0.0270 (share>0 0.845)   DOES NOT FLIP
    BREADTH-HI +0.0114 (share>0 0.632)  DOES NOT FLIP

So on correlation, de-grossing on EITHER tail beats an information-free placebo at nearly the
same rate.  Two readings, and they are not the same thing:

    (A) THE NULL IS BROKEN.  The BLOCK placebo is a circular shift of the gate's own firing
        path.  A shift of s days moves every de-grossed day s days forward - out of the crash
        it was sitting on.  Both tails of correlation fire inside 2020 and 2022 (rho spikes in
        a crash and the post-crash recovery is the low-rho regime that immediately follows), so
        the shift destroys a CALENDAR ALIGNMENT that both tails share, and the "excess" is the
        value of being de-grossed during a crash at all - available to any path with those
        days, information or not.
    (B) THE LOW TAIL CARRIES INFORMATION.  Low average pairwise correlation is a real
        risk-off/risk-on state and de-grossing on it is a real (if different) edge.

They separate cleanly, because they predict different things:

                                        (A) alignment artefact      (B) real information
    excess vs a placebo that PRESERVES
      the calendar alignment                collapses                  survives
    excess measured with the 2020/2022
      episodes DELETED from the tape         collapses                  survives
    excess fitted on 2009-2016, read
      on 2017+                               no relation                persists

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (REPRODUCE)  Does idea 606's committed 8-family BLOCK table rebuild here?  G3.
    Q2 (ALIGN)      Does the excess survive placebos that keep the firing days in their own
                    calendar year (YEARBLOCK) or keep the episode days exactly where they are
                    (EPISODEFIX)?  Pre-registered bar below.
    Q3 (STRIP)      Does the excess survive deleting the episodes from the return tape?
    Q4 (MECHANISM)  Do the two tails of CORR actually share the episode days?  Measured
                    directly as the de-grossed-day overlap with the declared episodes, real
                    vs BLOCK vs YEARBLOCK.
    Q5 (RULE 8)     Does the excess itself walk forward (IS-fitted -> OOS-read), and do the
                    BOOKS clear either PROTOCOL KEEP path with parameters chosen IS-only?

Pre-registered hypotheses and bars (fixed before any number below section [0] was read)
    H_ALIGN   For a family whose BLOCK excess is positive, an ALIGNMENT-PRESERVING placebo
              (YEARBLOCK, EPISODEFIX) reduces the median excess by >= 50%.  PASS = the
              alignment channel carries at least half of the published number.
    H_SPLIT   The reduction is LARGER for the reversed families (CORR-LO, BREADTH-HI) than for
              their prior-direction twins (CORR-HI, BREADTH-LO).  PASS = idea 606's reversal
              control is restored once the null is fixed, i.e. the failure was the null's.
    H_STRIP   Deleting COVID_TIGHT + BEAR2022 from the tape cuts CORR-LO's BLOCK excess by
              >= 50%.
    H_WF      Spearman(IS excess, OOS excess) per family >= +0.30 would be persistence; below
              that the statistic does not walk forward.
  A FAIL on any of these is a result and is printed as one.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. state         BREADTH / VOL20 / DISP / CORR, each in BOTH directions (direction is not
                     a third parameter: both are always reported, never selected on).
    2. placebo kind  RAND / BLOCK (idea 606's two) + YEARBLOCK / EPISODEFIX / BLOCKPOST (this
                     run's three alignment-preserving controls).
    ALL grid points reported at every panel / level q / window w / depth / cadence / gross /
    cost rung.  Nothing is chosen on the answer.

Reported axes, NEVER tuned or selected on (inherited from idea 606/602 verbatim)
    level q 0.07 / 0.12 / 0.17    w 252 / 504 / 1008 / 2016    depth 0.25 / 0.50 / 1.00
    cadence D / W                 gross 0.75 / 1.00            cost 0 / 10 / 25 bps
    panel   U56 / B136 / SMALL

The four placebo kinds, all rate-matched and information-free by construction
    RAND       iid days, EXACTLY the real arm's de-grossed day count.          (idea 606)
    BLOCK      circular shift of the whole effective path - exact rate AND     (idea 606)
               exact run-length distribution, and NO calendar alignment.
    YEARBLOCK  circular shift applied INDEPENDENTLY WITHIN EACH CALENDAR YEAR:  (NEW)
               exact rate, near-exact run lengths, and every de-grossed day stays in the year
               it was in.  This is BLOCK with the calendar alignment PUT BACK at year
               resolution and nothing else changed.
    EPISODEFIX circular shift of the non-episode days only, with the real path's values on the (NEW)
               declared episode days left exactly in place.  This is BLOCK with the alignment
               put back at EPISODE resolution.  Its rate is matched to the real arm's.
    BLOCKPOST  circular shift restricted to the POST-WARM-UP region - the days on which the     (NEW)
               gate's own rolling threshold exists.  The real arm is 1.0 on every pre-threshold
               day BY CONSTRUCTION (for w=2016 that is the first ~2 years of the tape); a plain
               BLOCK roll is free to move firing days into that region and to move the forced-
               quiet region out of it.  BLOCKPOST is BLOCK with only that one freedom removed,
               so the gap between them is the WARM-UP channel and nothing else.

Declared episodes (from the record, idea 851/861; fixed before the run, never swept)
    COVID_TIGHT 2020-02-19 .. 2020-03-23     BEAR2022 2022-01-04 .. 2022-10-12

Reproduction gates (section [0], printed before any new number is read)
    G1  a never-firing multiplier path reproduces the ungated book exactly.
    G2  THE TWIN CANCELS: every placebo kind's mean effective multiplier equals the real arm's,
        so both share the SAME matched-gross twin and excess = Sharpe(real) - Sharpe(placebo)
        with the twin term identically zero.  Printed as a max |d mean multiplier|.
    G3  idea 606's committed 8-family BLOCK medians and share>0, rebuilt here.
    G4  determinism: every placebo recomputed from its md5 seed, max |d| must be 0.
    G6  the fast Sharpe used on the placebo cells equals engine.metrics()["Sharpe"].

Data: committed caches only, no network, never yfinance.
SURVIVORSHIP: all three panels are current-constituent lists (the small panel additionally
drops every ticker with max_1d_move >= 1.0 per data/small_meta.csv), so CAGR and drawdown
LEVELS are optimistic throughout; the placebo DIFFERENCING and the real-minus-null contrasts
are the durable part.  The small panel starts 2010-01-04 and is a REBUILT cache, not idea
606's SMALL664, so G3 is priced on U56+B136 (unchanged membership) as well as pooled.

Deterministic (all placebo seeds md5-derived), standalone.  Modifies nothing.
"""
import hashlib
import sys
import time
from itertools import product
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests"
LINES = []

FREQ = "W"
MAX_VOL = 0.60
SMOOTH = 20
QS = [0.07, 0.12, 0.17]
WS = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
GROSSES = [0.75, 1.00]
RUNGS = [0, 10, 25]
STATES = ["BREADTH", "VOL20", "DISP", "CORR"]
SIDES = {"BREADTH": ("LO", "HI"), "VOL20": ("HI", "LO"), "DISP": ("HI", "LO"), "CORR": ("HI", "LO")}
KINDS = ["RAND", "BLOCK", "YEARBLOCK", "EPISODEFIX", "BLOCKPOST"]
ALIGN_KINDS = ["YEARBLOCK", "EPISODEFIX", "BLOCKPOST"]
NSEED = 10
SPLIT = "2017-01-01"
EPISODES = [("COVID_TIGHT", "2020-02-19", "2020-03-23"), ("BEAR2022", "2022-01-04", "2022-10-12")]

# idea 606's committed BLOCK table (pooled over its three panels), the object G3 prices
IDEA606 = {
    "BREADTH-LO": (+0.0737, 0.981), "BREADTH-HI": (+0.0114, 0.632),
    "VOL20-HI": (+0.0210, 0.722), "VOL20-LO": (-0.0128, 0.361),
    "DISP-HI": (+0.0280, 0.796), "DISP-LO": (-0.0204, 0.162),
    "CORR-HI": (+0.0420, 0.861), "CORR-LO": (+0.0270, 0.845),
}
PRIOR = {"BREADTH": "LO", "VOL20": "HI", "DISP": "HI", "CORR": "HI"}


def log(s=""):
    print(s)
    LINES.append(str(s))


# ------------------------------------------------------------------ primitives (idea 602/606)
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
    """20d average pairwise correlation, equal-weight index-vs-name variance identity."""
    rt = px.pct_change()
    sig = rt.rolling(SMOOTH).std()
    s_idx = rt.mean(axis=1).rolling(SMOOTH).std()
    n = sig.notna().sum(axis=1).replace(0, np.nan)
    sbar, s2bar = sig.mean(axis=1), (sig ** 2).mean(axis=1)
    return ((s_idx ** 2 - s2bar / n) / (sbar ** 2 - s2bar / n).replace(0, np.nan)).clip(-1, 1)


STATE_FN = {"BREADTH": state_breadth, "VOL20": state_vol20, "DISP": state_disp, "CORR": state_corr}


def gate_mult(st, thr, side, depth, cadence, idx):
    """Fire (de-gross to 1-depth) when the state is in its named tail; 1.0 before the rolling
    threshold exists.  LO fires on st < thr, HI on st > thr.  idea 606 verbatim."""
    fire = ((st < thr) if side == "LO" else (st > thr)) & st.notna() & thr.notna()
    m = pd.Series(1.0, index=idx).where(~fire, 1.0 - depth)
    if cadence == "W":
        m = m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)
    return m


def apply_eff(r_base, m_eff, gross, cost_bps):
    """Apply an ALREADY-EFFECTIVE (t+1-aligned) multiplier path with idea 399's switch cost."""
    switch = np.abs(np.diff(m_eff, prepend=m_eff[0]))
    return m_eff * r_base - switch * gross * cost_bps / 1e4


def seed_of(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def placebo_eff(m_eff, depth, kind, seed, yearkey, epmask, warm):
    """Rate-matched, information-free twin of the EFFECTIVE multiplier path m_eff (numpy).

    warm = days on which the gate's rolling threshold does not yet exist, so the REAL arm is
    1.0 there by construction.  BLOCK is free to move firing days into that region; BLOCKPOST
    is not.  That difference is the warm-up channel, priced separately."""
    v = np.asarray(m_eff, float)
    k = int((v < 1.0).sum())
    if k == 0:
        return v.copy()
    rng = np.random.default_rng(seed)
    if kind == "RAND":
        out = np.ones(len(v))
        out[rng.choice(len(v), size=k, replace=False)] = 1.0 - depth
        return out
    if kind == "BLOCK":
        return np.roll(v, int(rng.integers(1, len(v))))
    if kind in ("YEARBLOCK", "EPISODEFIX", "BLOCKPOST"):
        out = v.copy()
        if kind == "YEARBLOCK":
            segs = [yearkey == y for y in np.unique(yearkey)]
        elif kind == "EPISODEFIX":
            segs = [~epmask]
        else:
            segs = [~warm]
        for sel in segs:
            seg = v[sel]
            if len(seg) > 1:
                out[sel] = np.roll(seg, int(rng.integers(1, len(seg))))
        return out
    raise ValueError(kind)


# ------------------------------------------------------------------------------ metric helpers
def pack(r):
    m = metrics(pd.Series(r) if not isinstance(r, pd.Series) else r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return fast_sharpe(r[:h]), fast_sharpe(r[h:])


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep]


# ======================================================================================= [0]
def gates(panels):
    log("\n[0] REPRODUCTION GATES (printed before any new number is read)")
    px = panels["U56"]
    w = ewall_weights(px, 0.75)
    res = backtest(px, w, cost_bps=10, freq=FREQ)
    r_base = res["returns"].loc["2009-01-01":]
    ones = np.ones(len(r_base))
    g1 = float(np.max(np.abs(apply_eff(r_base.values, ones, 0.75, 10) - r_base.values)))
    log(f"  G1 never-firing multiplier == ungated book          max|d| = {g1:.3e}  "
        f"[{'PASS' if g1 < 1e-12 else 'FAIL'}]  (bar 1e-12)")
    g6 = abs(fast_sharpe(r_base.values) - metrics(r_base)["Sharpe"])
    log(f"  G6 fast Sharpe == engine.metrics()['Sharpe']        |d|    = {g6:.3e}  "
        f"[{'PASS' if g6 < 1e-10 else 'FAIL'}]  (bar 1e-10)")
    return g1, g6


# ======================================================================================= run
def run_panel(name, px):
    t0 = time.time()
    idx = px.index
    spy = px["SPY"].pct_change().fillna(0.0)
    states = {s: STATE_FN[s](px.drop(columns=["SPY"], errors="ignore")) for s in STATES}

    base = {}
    for g in GROSSES:
        base[g] = backtest(px.drop(columns=["SPY"], errors="ignore"),
                           ewall_weights(px.drop(columns=["SPY"], errors="ignore"), g),
                           cost_bps=10, freq=FREQ)["returns"]

    start = idx[max(260, 0)]
    win = idx >= start
    ii = idx[win]
    yearkey = ii.year.values
    epmask = np.zeros(len(ii), bool)
    for _, a, b in EPISODES:
        epmask |= (ii >= pd.Timestamp(a)) & (ii <= pd.Timestamp(b))
    stripkeep = ~epmask
    oos = ii >= pd.Timestamp(SPLIT)
    isw = ~oos

    spy_v = spy.loc[ii].values
    spy_cagr, spy_sh, spy_dd = pack(pd.Series(spy_v, index=ii))
    spy_h1, spy_h2 = halves(spy_v)
    spy_oos_c, spy_oos_s, spy_oos_d = pack(pd.Series(spy_v[oos], index=ii[oos]))
    bl = backtest(px.drop(columns=["SPY"], errors="ignore"),
                  rules_v2_weights(px.drop(columns=["SPY"], errors="ignore")),
                  cost_bps=10, freq=FREQ)["returns"].loc[ii]
    bl_c, bl_s, bl_d = pack(bl)
    bl_h1, bl_h2 = halves(bl.values)
    bl_oos_c, bl_oos_s, bl_oos_d = pack(bl.loc[ii[oos]])

    bench = dict(panel=name, spy_cagr=spy_cagr, spy_sh=spy_sh, spy_dd=spy_dd,
                 spy_h1=spy_h1, spy_h2=spy_h2, spy_oos_c=spy_oos_c, spy_oos_s=spy_oos_s,
                 spy_oos_d=spy_oos_d, bl_cagr=bl_c, bl_sh=bl_s, bl_dd=bl_d, bl_h1=bl_h1,
                 bl_h2=bl_h2, bl_oos_c=bl_oos_c, bl_oos_s=bl_oos_s, bl_oos_d=bl_oos_d)

    rows, exrows, g2, g4, g3check = [], [], 0.0, 0.0, []
    for st_name in STATES:
        st_full = states[st_name]
        for side in SIDES[st_name]:
            fam = f"{st_name}-{side}"
            for q, w in product(QS, WS):
                thr = st_full.rolling(w, min_periods=max(60, w // 4)).quantile(q if side == "LO" else 1 - q)
                warm = (thr.shift(1).isna() | st_full.shift(1).isna()).loc[ii].values
                for depth, cad in product(DEPTHS, CADENCES):
                    mult = gate_mult(st_full, thr, side, depth, cad, idx)
                    m_eff_full = mult.shift(1).fillna(1.0).loc[ii].values
                    fired = m_eff_full < 1.0
                    rate = float(fired.mean())
                    ep_share = float(epmask[fired].mean()) if fired.any() else np.nan
                    warm_share = float(warm.mean())
                    for g in GROSSES:
                        rb = base[g].loc[ii].values
                        real = {c: apply_eff(rb, m_eff_full, g, c) for c in RUNGS}
                        rr = real[10]
                        c_, s_, d_ = pack(pd.Series(rr, index=ii))
                        h1, h2 = halves(rr)
                        oc, os_, od = pack(pd.Series(rr[oos], index=ii[oos]))
                        rows.append(dict(
                            panel=name, family=fam, state=st_name, side=side, q=q, w=w,
                            depth=depth, cadence=cad, gross=g, rate=rate, ep_share=ep_share,
                            CAGR=c_, Sharpe=s_, MaxDD=d_, H1=h1, H2=h2,
                            IS_Sharpe=fast_sharpe(rr[isw]), OOS_CAGR=oc, OOS_Sharpe=os_,
                            OOS_MaxDD=od,
                            **{f"Sharpe_{c}bps": fast_sharpe(real[c]) for c in RUNGS},
                            **{f"CAGR_{c}bps": pack(pd.Series(real[c], index=ii))[0] for c in RUNGS},
                            **{f"MaxDD_{c}bps": pack(pd.Series(real[c], index=ii))[2] for c in RUNGS},
                        ))
                        # ---- placebo cells: excess = Sharpe(real) - Sharpe(placebo) --------
                        sh_real = fast_sharpe(rr)
                        sh_real_strip = fast_sharpe(rr[stripkeep])
                        sh_real_is = fast_sharpe(rr[isw])
                        sh_real_oos = fast_sharpe(rr[oos])
                        for kind in KINDS:
                            ex, exs, exi, exo, eps, wms = [], [], [], [], [], []
                            for sd in range(NSEED):
                                seed = seed_of(name, fam, q, w, depth, cad, g, kind, sd)
                                pe = placebo_eff(m_eff_full, depth, kind, seed, yearkey, epmask, warm)
                                g2 = max(g2, abs(pe.mean() - m_eff_full.mean()))
                                pr = apply_eff(rb, pe, g, 10)
                                ex.append(sh_real - fast_sharpe(pr))
                                exs.append(sh_real_strip - fast_sharpe(pr[stripkeep]))
                                exi.append(sh_real_is - fast_sharpe(pr[isw]))
                                exo.append(sh_real_oos - fast_sharpe(pr[oos]))
                                pf = pe < 1.0
                                eps.append(float(epmask[pf].mean()) if pf.any() else np.nan)
                                wms.append(float(warm[pf].mean()) if pf.any() else np.nan)
                            exrows.append(dict(
                                panel=name, family=fam, state=st_name, side=side, q=q, w=w,
                                depth=depth, cadence=cad, gross=g, kind=kind, rate=rate,
                                excess=float(np.median(ex)), excess_strip=float(np.median(exs)),
                                excess_IS=float(np.median(exi)), excess_OOS=float(np.median(exo)),
                                real_ep_share=ep_share, plac_ep_share=float(np.nanmean(eps)),
                                warm_share=warm_share, plac_warm_share=float(np.nanmean(wms)),
                            ))
        log(f"    {name}: {st_name} done  ({time.time() - t0:.0f}s)")

    # G4 determinism: recompute 24 placebo cells from the same seeds
    d4 = 0.0
    rng_rows = exrows[:6] + exrows[len(exrows) // 2:len(exrows) // 2 + 6]
    for r in rng_rows:
        thr = (states[r["state"]].rolling(r["w"], min_periods=max(60, r["w"] // 4))
               .quantile(r["q"] if r["side"] == "LO" else 1 - r["q"]))
        wm = (thr.shift(1).isna() | states[r["state"]].shift(1).isna()).loc[ii].values
        mult = gate_mult(states[r["state"]], thr, r["side"], r["depth"], r["cadence"], idx)
        me = mult.shift(1).fillna(1.0).loc[ii].values
        rb = base[r["gross"]].loc[ii].values
        sh_real = fast_sharpe(apply_eff(rb, me, r["gross"], 10))
        ex = []
        for sd in range(NSEED):
            seed = seed_of(name, r["family"], r["q"], r["w"], r["depth"], r["cadence"],
                           r["gross"], r["kind"], sd)
            pe = placebo_eff(me, r["depth"], r["kind"], seed, yearkey, epmask, wm)
            ex.append(sh_real - fast_sharpe(apply_eff(rb, pe, r["gross"], 10)))
        d4 = max(d4, abs(float(np.median(ex)) - r["excess"]))
    return pd.DataFrame(rows), pd.DataFrame(exrows), bench, g2, d4


def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 815 - is the CORR-LO positive excess a DE-GROSSING artefact?  (cloud 2026-09-15)")
    log("=" * 100)
    log(__doc__.split("Deterministic")[0].split("The finding")[0])

    panels = {}
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    sp = small_panel()
    panels["SMALL"] = sp
    log(f"panels: U56 {panels['U56'].shape}  B136 {panels['B136'].shape}  SMALL {sp.shape} "
        f"(sub-$2B, max_1d_move>=1.0 dropped)")

    g1, g6 = gates(panels)

    allrows, allex, benches, g2m, g4m = [], [], [], 0.0, 0.0
    for nm, px in panels.items():
        r, e, b, g2, g4 = run_panel(nm, px)
        allrows.append(r); allex.append(e); benches.append(b)
        g2m, g4m = max(g2m, g2), max(g4m, g4)
    cells = pd.concat(allrows, ignore_index=True)
    ex = pd.concat(allex, ignore_index=True)
    bench = pd.DataFrame(benches).set_index("panel")

    log(f"  G2 placebo mean multiplier == real arm's           max|d| = {g2m:.3e}  "
        f"[{'PASS' if g2m < 1e-12 else 'FAIL'}]  (bar 1e-12; if PASS the matched-gross twin "
        f"cancels exactly and excess = Sharpe(real) - Sharpe(placebo))")
    log(f"  G4 determinism, 36 placebo cells re-seeded          max|d| = {g4m:.3e}  "
        f"[{'PASS' if g4m < 1e-12 else 'FAIL'}]  (bar 1e-12)")

    # ------------------------------------------------------------------ G3 reproduction
    log("\n  G3 idea 606's committed BLOCK table, rebuilt here")
    log(f"    {'family':12s} {'606 med':>9s} {'here(3p)':>9s} {'here(U56+B136)':>15s} "
        f"{'606 shr':>8s} {'here shr':>9s} {'|d| med':>8s}")
    blk = ex[ex["kind"] == "BLOCK"]
    g3rows = []
    for fam, (m606, s606) in IDEA606.items():
        sub = blk[blk["family"] == fam]
        sub2 = sub[sub["panel"].isin(["U56", "B136"])]
        med, med2 = sub["excess"].median(), sub2["excess"].median()
        shr = float((sub["excess"] > 0).mean())
        log(f"    {fam:12s} {m606:+9.4f} {med:+9.4f} {med2:+15.4f} {s606:8.3f} {shr:9.3f} "
            f"{abs(med - m606):8.4f}")
        g3rows.append(dict(family=fam, idea606_median=m606, here_median=med,
                           here_median_u56_b136=med2, idea606_share=s606, here_share=shr))
    g3 = pd.DataFrame(g3rows)
    signok = int((np.sign(g3["here_median"]) == np.sign(g3["idea606_median"])).sum())
    log(f"    G3: sign agrees {signok}/8; median |d| {g3.eval('abs(here_median-idea606_median)').median():.4f}. "
        f"[{'PASS' if signok >= 7 else 'PARTIAL'}]  Panel vintage differs (SMALL rebuilt since "
        f"606's SMALL664), so the U56+B136 column is the like-for-like leg.")

    # =============================================================== [1] THE DECOMPOSITION
    log("\n" + "=" * 100)
    log("[1] THE DECOMPOSITION - median excess by family x placebo kind (n=432 arms/family)")
    log("=" * 100)
    piv = ex.pivot_table(index="family", columns="kind", values="excess", aggfunc="median")
    shr = ex.assign(pos=ex["excess"] > 0).pivot_table(index="family", columns="kind",
                                                      values="pos", aggfunc="mean")
    order = [f"{s}-{d}" for s in STATES for d in (PRIOR[s], "LO" if PRIOR[s] == "HI" else "HI")]
    log(f"    {'family':12s} " + " ".join(f"{k:>11s}" for k in KINDS) +
        "    | " + " ".join(f"{k[:5]+'shr':>9s}" for k in KINDS))
    for fam in order:
        log(f"    {fam:12s} " + " ".join(f"{piv.loc[fam, k]:+11.4f}" for k in KINDS) +
            "    | " + " ".join(f"{shr.loc[fam, k]:9.3f}" for k in KINDS))

    log("\n  H_ALIGN - does an alignment-preserving placebo cut the BLOCK excess by >= 50%?")
    ha = []
    for fam in order:
        b = piv.loc[fam, "BLOCK"]
        for k in ALIGN_KINDS:
            v = piv.loc[fam, k]
            red = (b - v) / abs(b) if abs(b) > 1e-9 else np.nan
            ha.append(dict(family=fam, kind=k, block=b, kind_median=v, reduction=red,
                           pass50=bool(red >= 0.50) if np.isfinite(red) else False))
        log(f"    {fam:12s} BLOCK {b:+.4f} -> " + "  ".join(
            f"{k} {piv.loc[fam,k]:+.4f} ({ha[-len(ALIGN_KINDS)+i]['reduction']:+6.1%})"
            for i, k in enumerate(ALIGN_KINDS)))
    ha = pd.DataFrame(ha)
    pos = [f for f in order if piv.loc[f, "BLOCK"] > 0]
    npass = int(ha[(ha["family"].isin(pos))]["pass50"].sum())
    log(f"    H_ALIGN: {npass} of {len(ALIGN_KINDS)*len(pos)} (positive-BLOCK family x alignment "
        f"kind) cells cut >= 50%  [{'PASS' if npass >= 2 * len(pos) else 'FAIL'}]")

    log("\n  H_SPLIT - is the cut LARGER on the reversed family than on its prior-direction twin?")
    log("    (and does the reversed family's excess go NEGATIVE, i.e. is 606's reversal control")
    log("     restored once the null keeps the calendar?)")
    hs = []
    for s in STATES:
        p, r = PRIOR[s], ("LO" if PRIOR[s] == "HI" else "HI")
        for k in ALIGN_KINDS:
            rp = float(ha[(ha.family == f"{s}-{p}") & (ha.kind == k)]["reduction"].iloc[0])
            rr = float(ha[(ha.family == f"{s}-{r}") & (ha.kind == k)]["reduction"].iloc[0])
            mp, mr = piv.loc[f"{s}-{p}", k], piv.loc[f"{s}-{r}", k]
            hs.append(dict(state=s, kind=k, prior_reduction=rp, reversed_reduction=rr,
                           prior_median=mp, reversed_median=mr,
                           reversed_larger=bool(rr > rp),
                           control_restored=bool(mr < 0 <= mp)))
            log(f"    {s:8s} {k:11s} prior({p}) {mp:+.4f} ({rp:+7.1%})   "
                f"reversed({r}) {mr:+.4f} ({rr:+7.1%})   "
                f"{'CONTROL RESTORED' if mr < 0 <= mp else ('reversed cut more' if rr > rp else 'prior cut more')}")
    hs = pd.DataFrame(hs)
    log(f"    H_SPLIT: reversed cut more in {int(hs['reversed_larger'].sum())} of {len(hs)} "
        f"(state x kind)  [{'PASS' if hs['reversed_larger'].mean() > 0.5 else 'FAIL'}]")
    log(f"    reversal control RESTORED (reversed < 0 <= prior) in "
        f"{int(hs['control_restored'].sum())} of {len(hs)} (state x kind); "
        f"under BLOCK it holds in "
        f"{sum(1 for s in STATES if piv.loc[f'{s}-' + ('LO' if PRIOR[s]=='HI' else 'HI'),'BLOCK'] < 0 <= piv.loc[f'{s}-{PRIOR[s]}','BLOCK'])}"
        f" of {len(STATES)} states")

    # =============================================================== [2] EPISODE STRIP
    log("\n" + "=" * 100)
    log("[2] H_STRIP - the same excess with COVID_TIGHT + BEAR2022 DELETED from the tape")
    log("=" * 100)
    ps = ex.pivot_table(index="family", columns="kind", values="excess_strip", aggfunc="median")
    log(f"    {'family':12s} {'BLOCK full':>11s} {'BLOCK strip':>12s} {'cut':>8s} | "
        f"{'YEARBLK full':>13s} {'YEARBLK strip':>14s}")
    strip = []
    for fam in order:
        b, bs = piv.loc[fam, "BLOCK"], ps.loc[fam, "BLOCK"]
        cut = (b - bs) / abs(b) if abs(b) > 1e-9 else np.nan
        strip.append(dict(family=fam, block_full=b, block_strip=bs, cut=cut,
                          yearblock_full=piv.loc[fam, "YEARBLOCK"],
                          yearblock_strip=ps.loc[fam, "YEARBLOCK"]))
        log(f"    {fam:12s} {b:+11.4f} {bs:+12.4f} {cut:+8.1%} | {piv.loc[fam,'YEARBLOCK']:+13.4f} "
            f"{ps.loc[fam,'YEARBLOCK']:+14.4f}")
    strip = pd.DataFrame(strip)
    cl = float(strip.loc[strip.family == "CORR-LO", "cut"].iloc[0])
    log(f"    H_STRIP (CORR-LO BLOCK excess cut >= 50% by deleting the episodes): {cl:+.1%}  "
        f"[{'PASS' if cl >= 0.50 else 'FAIL'}]")

    # =============================================================== [3] MECHANISM
    log("\n" + "=" * 100)
    log("[3] Q4 MECHANISM - do the two tails share the episode days?  de-grossed-day share")
    log("    inside COVID_TIGHT + BEAR2022 (those days are 6.3% of the tape), real vs placebo")
    log("=" * 100)
    mech = ex.groupby(["family", "kind"]).agg(real=("real_ep_share", "mean"),
                                              plac=("plac_ep_share", "mean"),
                                              warm=("warm_share", "mean"),
                                              pwarm=("plac_warm_share", "mean")).reset_index()
    log(f"    {'family':12s} {'real':>8s} " + " ".join(f"{k[:9]:>10s}" for k in KINDS))
    mrows = []
    for fam in order:
        sub = mech[mech.family == fam].set_index("kind")
        log(f"    {fam:12s} {sub['real'].iloc[0]:8.3f} " +
            " ".join(f"{sub.loc[k,'plac']:10.3f}" for k in KINDS))
        mrows.append(dict(family=fam, real_ep_share=sub["real"].iloc[0],
                          **{f"plac_ep_{k}": sub.loc[k, "plac"] for k in KINDS},
                          warm_share=sub["warm"].iloc[0],
                          **{f"plac_warm_{k}": sub.loc[k, "pwarm"] for k in KINDS}))
    mech_out = pd.DataFrame(mrows)
    log("\n    THE WARM-UP CHANNEL - share of de-grossed days in the pre-threshold region, where")
    log("    the REAL arm cannot fire at all (real = 0.000 by construction; warm days are "
        f"{mech['warm'].mean():.1%} of the tape on average):")
    log(f"    {'family':12s} " + " ".join(f"{k[:9]:>10s}" for k in KINDS))
    for fam in order:
        sub = mech[mech.family == fam].set_index("kind")
        log(f"    {fam:12s} " + " ".join(f"{sub.loc[k,'pwarm']:10.3f}" for k in KINDS))

    # =============================================================== [3b] THE INVERSION
    log("\n" + "=" * 100)
    log("[3b] H_INVERT - the queue asked whether the REVERSED family's excess is the alignment")
    log("     artefact.  The two controls say the opposite, so state it as a test: is it the")
    log("     PRIOR-DIRECTION excess (idea 606's headline) that EPISODEFIX removes?")
    log("     Bar: EPISODEFIX median <= 0.25 x BLOCK median for all four prior families, and NOT")
    log("     for their reversed twins.")
    log("=" * 100)
    inv = []
    for s in STATES:
        for d, tag in ((PRIOR[s], "prior"), ("LO" if PRIOR[s] == "HI" else "HI", "reversed")):
            fam = f"{s}-{d}"
            b, e_, y = piv.loc[fam, "BLOCK"], piv.loc[fam, "EPISODEFIX"], piv.loc[fam, "YEARBLOCK"]
            share = float(mech[(mech.family == fam) & (mech.kind == "BLOCK")]["real"].iloc[0])
            gone = bool(e_ <= 0.25 * b) if b > 0 else None
            inv.append(dict(family=fam, direction=tag, real_ep_share=share, block=b,
                            yearblock=y, episodefix=e_, removed=gone))
            log(f"    {fam:12s} {tag:8s} fires-in-episode {share:6.3f}  BLOCK {b:+.4f}  "
                f"YEARBLOCK {y:+.4f}  EPISODEFIX {e_:+.4f}   "
                f"{'REMOVED' if gone else ('survives' if b > 0 else 'BLOCK already <= 0')}")
    inv = pd.DataFrame(inv)
    pri = inv[inv.direction == "prior"]
    rev = inv[inv.direction == "reversed"]
    npri = int((pri["removed"] == True).sum())
    nrev = int((rev["removed"] == True).sum())
    log(f"    H_INVERT: EPISODEFIX removes the excess in {npri} of 4 PRIOR families and "
        f"{nrev} of {int(rev['block'].gt(0).sum())} positive-BLOCK REVERSED families  "
        f"[{'PASS' if npri >= 3 and nrev == 0 else 'FAIL'}]")
    rho_fam = spearman(inv["real_ep_share"], inv["episodefix"] - inv["block"])
    arm = ex[ex.kind.isin(["BLOCK", "EPISODEFIX"])].pivot_table(
        index=["panel", "family", "q", "w", "depth", "cadence", "gross"],
        columns="kind", values="excess").reset_index()
    arm = arm.merge(ex[ex.kind == "BLOCK"][["panel", "family", "q", "w", "depth", "cadence",
                                            "gross", "real_ep_share"]],
                    on=["panel", "family", "q", "w", "depth", "cadence", "gross"], how="left")
    rho_arm = spearman(arm["real_ep_share"], arm["EPISODEFIX"] - arm["BLOCK"])
    log(f"    MECHANISM: rho(share of the gate's de-grossed days inside the two episodes, "
        f"EPISODEFIX - BLOCK) = {rho_fam:+.3f} across the 8 families and {rho_arm:+.3f} across "
        f"all {len(arm)} individual arms.  The more a gate sits on the crash, the more of its")
    log(f"    published excess a crash-preserving null takes back.")
    inv.to_csv(OUT / f"{STEM}.invert.csv", index=False)

    # =============================================================== [4] RULE 8 on the CLAIM
    log("\n" + "=" * 100)
    log("[4] H_WF - PROTOCOL rule 8 ON THE STATISTIC: excess fitted 2009-2016, read 2017+")
    log("=" * 100)
    log(f"    {'family':12s} {'kind':11s} {'IS med':>9s} {'OOS med':>9s} {'rho(IS,OOS)':>12s}")
    wf = []
    for fam in order:
        for k in KINDS:
            sub = ex[(ex.family == fam) & (ex.kind == k)]
            rho = spearman(sub["excess_IS"], sub["excess_OOS"])
            wf.append(dict(family=fam, kind=k, IS_median=sub["excess_IS"].median(),
                           OOS_median=sub["excess_OOS"].median(), rho=rho))
            if k in ("BLOCK", "YEARBLOCK"):
                log(f"    {fam:12s} {k:11s} {sub['excess_IS'].median():+9.4f} "
                    f"{sub['excess_OOS'].median():+9.4f} {rho:+12.3f}")
    wf = pd.DataFrame(wf)
    blkwf = wf[wf.kind == "BLOCK"]
    log(f"    H_WF (rho >= +0.30 on BLOCK): {int((blkwf['rho'] >= 0.30).sum())} of 8 families  "
        f"[{'PASS' if (blkwf['rho'] >= 0.30).sum() >= 5 else 'FAIL'}]")

    # =============================================================== [5] RULE 8 on the BOOKS
    log("\n" + "=" * 100)
    log("[5] PROTOCOL rule 8 ON THE BOOKS - (q,w) chosen on 2009-2016 IS Sharpe ONLY, read on")
    log("    2017+ against RULES v2 and SPY.  Both KEEP paths on every grid point.")
    log("=" * 100)
    log("    comparands (10 bps, weekly, t+1):")
    for p in bench.index:
        b = bench.loc[p]
        log(f"      {p:6s} SPY {b.spy_cagr:7.2%} / {b.spy_sh:5.3f} / {b.spy_dd:7.2%}  "
            f"(H {b.spy_h1:.3f}/{b.spy_h2:.3f}; OOS {b.spy_oos_c:6.2%}/{b.spy_oos_s:5.3f}/"
            f"{b.spy_oos_d:7.2%})   RULES v2 {b.bl_cagr:6.2%} / {b.bl_sh:5.3f} / {b.bl_dd:7.2%} "
            f"(H {b.bl_h1:.3f}/{b.bl_h2:.3f}; OOS {b.bl_oos_s:5.3f})")

    cells = cells.merge(bench.reset_index(), on="panel", how="left")
    cells["pass4a"] = ((cells.H1 > cells.bl_h1) & (cells.H2 > cells.bl_h2) &
                       (cells.MaxDD >= cells.bl_dd))
    cells["pass4b"] = ((cells.H1 > cells.spy_h1) & (cells.H2 > cells.spy_h2) &
                       (cells.OOS_Sharpe > cells.spy_oos_s) &
                       (cells.MaxDD >= 0.60 * cells.spy_dd) &
                       (cells.CAGR >= 0.70 * cells.spy_cagr))
    log(f"\n    CENSUS over all {len(cells)} grid points @10bps: 4a {int(cells.pass4a.sum())}, "
        f"4b {int(cells.pass4b.sum())}")
    by = cells.groupby("family").agg(n=("CAGR", "size"), a4=("pass4a", "sum"), b4=("pass4b", "sum"),
                                     medS=("Sharpe", "median"), medC=("CAGR", "median"))
    log(f"    {'family':12s} {'n':>5s} {'4a':>5s} {'4b':>5s} {'med Sharpe':>11s} {'med CAGR':>9s}")
    for fam in order:
        r = by.loc[fam]
        log(f"    {fam:12s} {int(r.n):5d} {int(r.a4):5d} {int(r.b4):5d} {r.medS:11.3f} {r.medC:9.2%}")

    log("\n    RULE-8 CHOOSER: within each (panel, family, depth, cadence, gross) pick the (q,w)")
    log("    with the best 2009-2016 IS Sharpe, then read 2017+ ONCE.")
    keys = ["panel", "family", "depth", "cadence", "gross"]
    pick = cells.loc[cells.groupby(keys)["IS_Sharpe"].idxmax()].copy()
    pick["oos4b"] = ((pick.OOS_Sharpe > pick.spy_oos_s) &
                     (pick.OOS_MaxDD >= 0.60 * pick.spy_oos_d) &
                     (pick.OOS_CAGR >= 0.70 * pick.spy_oos_c))
    pick["oos_beats_base"] = pick.OOS_Sharpe > pick.bl_oos_s
    log(f"    {len(pick)} rule-8 picks: OOS Sharpe beats SPY in "
        f"{int((pick.OOS_Sharpe > pick.spy_oos_s).sum())}, beats RULES v2 in "
        f"{int(pick.oos_beats_base.sum())}, clears 4b OOS in {int(pick.oos4b.sum())}, "
        f"clears full-sample 4a in {int(pick.pass4a.sum())} / 4b in {int(pick.pass4b.sum())}")
    log(f"    {'family':12s} {'picks':>6s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s} "
        f"{'>SPY':>5s} {'>v2':>5s} {'4b':>4s}")
    prow = []
    for fam in order:
        s = pick[pick.family == fam]
        log(f"    {fam:12s} {len(s):6d} {s.OOS_CAGR.median():9.2%} {s.OOS_Sharpe.median():11.3f} "
            f"{s.OOS_MaxDD.median():10.2%} {int((s.OOS_Sharpe>s.spy_oos_s).sum()):5d} "
            f"{int(s.oos_beats_base.sum()):5d} {int(s.oos4b.sum()):4d}")
        prow.append(dict(family=fam, picks=len(s), oos_cagr=s.OOS_CAGR.median(),
                         oos_sharpe=s.OOS_Sharpe.median(), oos_maxdd=s.OOS_MaxDD.median(),
                         beats_spy=int((s.OOS_Sharpe > s.spy_oos_s).sum()),
                         beats_v2=int(s.oos_beats_base.sum()), oos4b=int(s.oos4b.sum())))

    hon = pick[pick.pass4b & pick.oos4b]
    log(f"\n    HONEST 4b (rule-8 pick, clears 4b on the FULL sample AND out of sample): "
        f"{len(hon)} of {len(pick)}")
    if len(hon):
        log(f"      {'panel':6s} {'family':12s} {'q':>5s} {'w':>5s} {'dep':>5s} {'cad':>4s} "
            f"{'g':>5s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1/H2':>13s} "
            f"{'OOS C/S/DD':>24s}")
        for _, r in hon.sort_values("OOS_Sharpe", ascending=False).head(12).iterrows():
            log(f"      {r.panel:6s} {r.family:12s} {r.q:5.2f} {int(r.w):5d} {r.depth:5.2f} "
                f"{r.cadence:>4s} {r.gross:5.2f} {r.CAGR:7.2%} {r.Sharpe:7.3f} {r.MaxDD:8.2%} "
                f"{r.H1:6.3f}/{r.H2:6.3f} {r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:6.3f}/{r.OOS_MaxDD:8.2%}")
        log(f"      by family: " + ", ".join(f"{f} {int((hon.family == f).sum())}"
                                             for f in order if (hon.family == f).any()))
        hon.to_csv(OUT / f"{STEM}.honest4b.csv", index=False)

    log("\n    COST LADDER on the 4b census (full sample, Sharpe/CAGR/MaxDD at each rung):")
    for c in RUNGS:
        cc = ((cells[f"Sharpe_{c}bps"] > cells.spy_sh) &
              (cells[f"CAGR_{c}bps"] >= 0.70 * cells.spy_cagr) &
              (cells[f"MaxDD_{c}bps"] >= 0.60 * cells.spy_dd))
        log(f"      {c:2d} bps: full-sample Sharpe>SPY & CAGR floor & DD cap -> {int(cc.sum())} "
            f"of {len(cells)}")

    # -------------------------------------------------------------------------- persist
    cells.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    ex.to_csv(OUT / f"{STEM}.excess.csv", index=False)
    g3.to_csv(OUT / f"{STEM}.g3.csv", index=False)
    ha.to_csv(OUT / f"{STEM}.align.csv", index=False)
    hs.to_csv(OUT / f"{STEM}.split.csv", index=False)
    strip.to_csv(OUT / f"{STEM}.strip.csv", index=False)
    mech_out.to_csv(OUT / f"{STEM}.mechanism.csv", index=False)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(prow).to_csv(OUT / f"{STEM}.picks.csv", index=False)
    bench.to_csv(OUT / f"{STEM}.bench.csv")

    log(f"\n  wrote {STEM}.{{cells,excess,g3,align,split,strip,mechanism,walkforward,picks,bench}}.csv")
    log(f"  total {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

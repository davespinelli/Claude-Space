#!/usr/bin/env python3
"""Idea 870 - "is-the-CORR-LO-excess-a-VOL-TARGET-in-disguise" (lane B, 2026-09-15).

The finding this run exists to explain
--------------------------------------
Idea 815 (cloud + lane C, both independently) left one survivor on an eight-family sweep of
placebo-differenced de-grossing gates:

    CORR-LO is the ONLY family of eight whose placebo excess WALKS FORWARD
        rho(IS excess, OOS excess) = +0.392 (BLOCK) / +0.468 (YEARBLOCK),
        IS +0.0414 -> OOS +0.0269 and IS +0.0577 -> OOS +0.0572,
    and it is the ONLY family with ZERO 4b passes in its 432 books (4a 0/432, 4b 0/432),
    against CORR-HI's 131 of 432 - whose excess EPISODEFIX erases entirely.

So the record holds a Sharpe edge that persists out of sample and buys no capital at all.  The
queue's hypothesis for what it actually is: de-grossing on low average pairwise correlation is
a REALISED-VOL TARGET in disguise, priced at a worse cost.

The hypothesis has a mechanical basis, and that is why it is worth pricing.  `state_corr`
in the record is built from the equal-weight variance identity

    corr_t  =  (s_idx^2 - s2bar/n) / (sbar^2 - s2bar/n),        s_idx = 20d vol of the EW book

so average pairwise correlation is, ALGEBRAICALLY, the PORTFOLIO variance divided by the
average NAME variance.  Firing on low corr is therefore firing on a low ratio, which at roughly
constant name vol IS firing on low portfolio vol.  If that is all it is, then replacing the
CORR state by realised portfolio vol should reproduce the gate, the excess and the books - and
a null that holds the realised-vol regime fixed should erase the excess the way EPISODEFIX
erased the other four families'.

The record already prices one half of the decomposition and it points the other way: the
average-NAME-vol family VOL20-LO has excess -0.0176, i.e. NEGATIVE, while CORR-LO is +0.0341.
If portfolio vol carries it, PORTVOL-LO must look like CORR-LO and not like VOL20-LO.

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (REPRODUCE) Does idea 815's committed CORR table rebuild here?  G3.
    Q2 (LEG)       Is the excess a MEAN leg (the gate sits out bad returns) or a VOL leg (the
                   gate shrinks the denominator)?  Decomposed EXACTLY, no residual.
    Q3 (SPAN)      Does a realised-vol target reproduce CORR-LO's firing path, at every matched
                   grid point?  Measured as Jaccard of de-grossed days and rho of the paths.
    Q4 (NULL)      Does the excess survive a placebo that holds the REALISED-VOL REGIME fixed
                   (VOLBLOCK), the way the other four families did not survive EPISODEFIX?
    Q5 (COST)      At matched realised gross, does a vol target deliver CORR-LO's Sharpe at
                   every cost rung with LESS gate turnover?  ("priced at a worse cost")
    Q6 (RULE 8)    Does the excess walk forward, and do the BOOKS clear either PROTOCOL KEEP
                   path with parameters chosen IS-only (2009-2016), read once on 2017+?

Pre-registered hypotheses and bars (fixed before any number below section [0] was read)
    H_LEG    The VOL leg carries >= 50% of CORR-LO's median BLOCK excess.
             PASS = the excess is arithmetically a denominator effect, as a vol target is.
    H_SPAN   For at least one vol-target form, the median over matched arms of the de-grossed-
             day Jaccard against CORR-LO is >= 0.50.  PASS = same gate, different name.
    H_NULL   VOLBLOCK - a rate- and run-length-matched circular shift applied WITHIN realised
             portfolio-vol terciles, so every placebo firing day sits in the same vol regime
             as a real one - cuts CORR-LO's median BLOCK excess by >= 50%.
             PASS = the excess is the vol regime and not the correlation.
    H_COST   At matched realised gross the best-spanning vol-target form's Sharpe is >= CORR-LO's
             at ALL THREE cost rungs AND CORR-LO's gate turnover is strictly higher.
             PASS = the queue's "priced at a worse cost" reading.
    H_WF     rho(IS excess, OOS excess) >= +0.30 for CORR-LO (reproducing 815's +0.392) AND for
             the best-spanning vol-target form.  PASS = the persistence is a property of the
             vol state, not of correlation.
  A FAIL on any of these is a result and is printed as one.  Nothing is re-specified after a bar
  is read.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. target form   PORTVOL-GATE (binary quantile gate on realised EW-book vol),
                     NAMEVOL-GATE (binary quantile gate on average NAME vol = the record's
                                   VOL20 state, carried as the decomposition's other half),
                     VTCONT       (continuous m = clip(sigma_target/sigma_t, 1-depth, 1), the
                                   textbook vol target).
    2. cost rung     0 / 10 / 25 bps.
    ALL grid points reported at every panel / level q / window w / depth / cadence / gross.
    Nothing is chosen on the answer.

Reported axes, NEVER tuned or selected on (inherited from ideas 602/606/815 verbatim)
    level q 0.07 / 0.12 / 0.17     w 252 / 504 / 1008 / 2016     depth 0.25 / 0.50 / 1.00
    cadence D / W                  gross 0.75 / 1.00             panel U56 / B136 / SMALL
    SIDE (LO / HI) is not a third parameter: both sides of every state are always reported and
    never selected on, exactly as idea 815 declared it.

The placebo kinds, all rate-matched and information-free by construction
    BLOCK      circular shift of the whole effective path - exact rate AND exact run-length
               distribution, no calendar alignment.                          (ideas 606 / 815)
    YEARBLOCK  circular shift INDEPENDENTLY WITHIN EACH CALENDAR YEAR.       (idea 815)
    VOLBLOCK   circular shift INDEPENDENTLY WITHIN EACH REALISED-VOL TERCILE  (NEW, this run)
               of the ungated equal-weight book.  Exact per-tercile firing count, near-exact
               run lengths, and every de-grossed day stays in the vol regime it was in.  This
               is BLOCK with the VOL REGIME PUT BACK and nothing else changed - the exact
               analogue of what EPISODEFIX did to the calendar in idea 815.
    Terciles are full-sample cuts of a state the null never trades; like idea 815's declared
    episodes they are a measurement device, not a tradeable path.  Stated, not hidden.

Reproduction gates (section [0], printed before any new number is read)
    G1  a never-firing multiplier path reproduces the ungated book exactly.
    G2  THE TWIN CANCELS: every placebo kind's mean effective multiplier equals the real arm's,
        so excess = Sharpe(real) - Sharpe(placebo) with the matched-gross twin term zero.
    G3  idea 815's committed CORR-HI / CORR-LO BLOCK and YEARBLOCK medians, rebuilt here.
    G4  determinism: every placebo recomputed from its md5 seed, max |d| must be 0.
    G5  the fast Sharpe used on the placebo cells equals engine.metrics()["Sharpe"].
    G6  the mean/vol decomposition is EXACT: MEANLEG + VOLLEG - excess == 0 on every cell.

Data: committed caches only, no network, never yfinance.
SURVIVORSHIP: all three panels are current-constituent lists (the small panel additionally
drops every ticker with max_1d_move >= 1.0 per data/small_meta.csv), so CAGR and drawdown
LEVELS are optimistic throughout; the placebo DIFFERENCING and the real-minus-null contrasts
are the durable part.

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
NSEED = 10
SPLIT = "2017-01-01"

# binary quantile-gate states.  CORR is the record's; PORTVOL and NAMEVOL are the two halves of
# the variance identity that defines it.  Both sides of each are always reported.
GATE_STATES = ["CORR", "PORTVOL", "NAMEVOL"]
SIDES = ("LO", "HI")
KINDS = ["BLOCK", "YEARBLOCK", "VOLBLOCK"]
# the three target forms named by the queue (parameter 1)
FORMS = ["PORTVOL-GATE", "NAMEVOL-GATE", "VTCONT"]

# idea 815's committed CORR medians (cloud result.md table [1], pooled over its three panels)
IDEA815 = {("CORR-HI", "BLOCK"): +0.0554, ("CORR-HI", "YEARBLOCK"): +0.0249,
           ("CORR-LO", "BLOCK"): +0.0341, ("CORR-LO", "YEARBLOCK"): +0.0568}
IDEA815_EP = {"CORR-HI": 0.186, "CORR-LO": 0.001}
IDEA815_WF = {"CORR-LO-BLOCK": +0.392, "CORR-LO-YEARBLOCK": +0.468}


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


def mu_sigma(v):
    v = np.asarray(v, float)
    return v.mean() * 252, v.std(ddof=1) * np.sqrt(252)


def state_namevol(px):
    """Average NAME vol - identical to idea 606/815's VOL20 state."""
    return (px.pct_change().rolling(SMOOTH).std() * np.sqrt(252)).mean(axis=1)


def state_portvol(px):
    """Realised vol of the equal-weight book - the vol a vol target actually targets."""
    return px.pct_change().mean(axis=1).rolling(SMOOTH).std() * np.sqrt(252)


def state_corr(px):
    """20d average pairwise correlation, equal-weight index-vs-name variance identity.
    Verbatim from idea 815 / baseline-side record; note corr = (portvol^2 - .)/(namevol^2 - .)."""
    rt = px.pct_change()
    sig = rt.rolling(SMOOTH).std()
    s_idx = rt.mean(axis=1).rolling(SMOOTH).std()
    n = sig.notna().sum(axis=1).replace(0, np.nan)
    sbar, s2bar = sig.mean(axis=1), (sig ** 2).mean(axis=1)
    return ((s_idx ** 2 - s2bar / n) / (sbar ** 2 - s2bar / n).replace(0, np.nan)).clip(-1, 1)


STATE_FN = {"CORR": state_corr, "PORTVOL": state_portvol, "NAMEVOL": state_namevol}


def gate_mult(st, thr, side, depth, cadence, idx):
    """Fire (de-gross to 1-depth) when the state is in its named tail; 1.0 before the rolling
    threshold exists.  LO fires on st < thr, HI on st > thr.  idea 606/815 verbatim."""
    fire = ((st < thr) if side == "LO" else (st > thr)) & st.notna() & thr.notna()
    m = pd.Series(1.0, index=idx).where(~fire, 1.0 - depth)
    if cadence == "W":
        m = m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)
    return m


def vtcont_mult(st, thr, side, depth, cadence, idx):
    """Textbook continuous vol target on the realised portfolio vol.
    HI: m = clip(sigma_target/sigma_t, 1-depth, 1) with sigma_target the rolling (1-q) level -
        cut gross as vol runs hot, never lever.
    LO: m = clip(sigma_t/sigma_target, 1-depth, 1) with sigma_target the rolling q level - the
        SIGN-MATCH to CORR-LO, i.e. cut gross as vol runs cold.
    1.0 before the rolling level exists, same warm-up convention as the binary gates."""
    ratio = (thr / st) if side == "HI" else (st / thr)
    m = ratio.clip(upper=1.0).clip(lower=1.0 - depth)
    m = m.where(st.notna() & thr.notna(), 1.0).reindex(idx).fillna(1.0)
    if cadence == "W":
        m = m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)
    return m


def apply_eff(r_base, m_eff, gross, cost_bps):
    """Apply an ALREADY-EFFECTIVE (t+1-aligned) multiplier path with idea 399's switch cost."""
    switch = np.abs(np.diff(m_eff, prepend=m_eff[0]))
    return m_eff * r_base - switch * gross * cost_bps / 1e4


def gate_turnover(m_eff):
    """Annualised one-way gate turnover: the part of the book's trading the GATE causes."""
    return float(np.abs(np.diff(m_eff, prepend=m_eff[0])).sum() * 252 / len(m_eff))


def seed_of(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def placebo_eff(m_eff, kind, seed, yearkey, volkey):
    """Rate-matched, information-free twin of the EFFECTIVE multiplier path m_eff (numpy).
    Segment-wise np.roll preserves each segment's multiset exactly, so the per-segment firing
    count is EXACT and the pooled mean multiplier is exact for every kind."""
    v = np.asarray(m_eff, float)
    if (v < 1.0).sum() == 0:
        return v.copy()
    rng = np.random.default_rng(seed)
    if kind == "BLOCK":
        return np.roll(v, int(rng.integers(1, len(v))))
    segs = yearkey if kind == "YEARBLOCK" else volkey
    out = v.copy()
    for key in np.unique(segs):
        sel = segs == key
        seg = v[sel]
        if len(seg) > 1:
            out[sel] = np.roll(seg, int(rng.integers(1, len(seg))))
    return out


# ------------------------------------------------------------------------------ metric helpers
def pack(r, idx=None):
    s = r if isinstance(r, pd.Series) else pd.Series(r, index=idx)
    m = metrics(s)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return fast_sharpe(r[:h]), fast_sharpe(r[h:])


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra, rb = pd.Series(a[ok]).rank().values, pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def pearson(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.std() == 0 or b.std() == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def jaccard(a, b):
    a, b = np.asarray(a, bool), np.asarray(b, bool)
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else np.nan


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]]


def keep_paths(c, s, dd, h1, h2, bl, spy):
    """PROTOCOL rule 4.  4a vs the LIVE book (RULES v2), 4b vs SPY."""
    a = (h1 > bl["h1"]) and (h2 > bl["h2"]) and (dd >= bl["dd"])
    b = (h1 > spy["h1"]) and (h2 > spy["h2"]) and (dd >= 0.60 * spy["dd"]) and (c >= 0.70 * spy["c"])
    return a, b


# ======================================================================================= [0]
def gates_pre(panels):
    log("\n[0] REPRODUCTION GATES (printed before any new number is read)")
    px = panels["U56"].drop(columns=["SPY"], errors="ignore")
    r_base = backtest(px, ewall_weights(px, 0.75), cost_bps=10, freq=FREQ)["returns"].loc["2009-01-01":]
    ones = np.ones(len(r_base))
    g1 = float(np.max(np.abs(apply_eff(r_base.values, ones, 0.75, 10) - r_base.values)))
    log(f"  G1 never-firing multiplier == ungated book       max|d| = {g1:.3e}  "
        f"[{'PASS' if g1 < 1e-12 else 'FAIL'}]  (bar 1e-12)")
    g5 = abs(fast_sharpe(r_base.values) - metrics(r_base)["Sharpe"])
    log(f"  G5 fast Sharpe == engine.metrics()['Sharpe']     |d|    = {g5:.3e}  "
        f"[{'PASS' if g5 < 1e-10 else 'FAIL'}]  (bar 1e-10)")
    return g1, g5


# ======================================================================================= run
def run_panel(name, px, arms, cells):
    t0 = time.time()
    core = px.drop(columns=["SPY"], errors="ignore")
    idx = px.index
    states = {s: STATE_FN[s](core) for s in GATE_STATES}

    base = {g: backtest(core, ewall_weights(core, g), cost_bps=10, freq=FREQ)["returns"]
            for g in GROSSES}

    ii = idx[idx >= idx[260]]
    yearkey = ii.year.values
    oos = (ii >= pd.Timestamp(SPLIT)).values if hasattr(ii >= pd.Timestamp(SPLIT), "values") \
        else np.asarray(ii >= pd.Timestamp(SPLIT))
    isw = ~oos

    # --- the VOLBLOCK segmentation: realised-vol terciles of the UNGATED equal-weight book ---
    pv = states["PORTVOL"].loc[ii]
    cuts = pv.quantile([1 / 3, 2 / 3]).values
    volkey = np.digitize(pv.fillna(pv.median()).values, cuts)

    spy_v = px["SPY"].pct_change().fillna(0.0).loc[ii].values
    sc, ss, sd = pack(spy_v, ii)
    sh1, sh2 = halves(spy_v)
    soc, sos, sod = pack(spy_v[oos], ii[oos])
    soh1, soh2 = halves(spy_v[oos])
    bl_r = backtest(core, rules_v2_weights(core), cost_bps=10, freq=FREQ)["returns"].loc[ii]
    bc, bs, bd = pack(bl_r)
    bh1, bh2 = halves(bl_r.values)
    boc, bos, bod = pack(bl_r.loc[ii[oos]])
    boh1, boh2 = halves(bl_r.loc[ii[oos]].values)
    bench = dict(panel=name,
                 spy=dict(c=sc, s=ss, dd=sd, h1=sh1, h2=sh2),
                 spy_oos=dict(c=soc, s=sos, dd=sod, h1=soh1, h2=soh2),
                 bl=dict(c=bc, s=bs, dd=bd, h1=bh1, h2=bh2),
                 bl_oos=dict(c=boc, s=bos, dd=bod, h1=boh1, h2=boh2))

    g2 = g4 = g6 = 0.0
    paths = {}                      # (q,w,depth,cad) -> {family: fired boolean vector}

    build = [(f"{s}-{side}", s, side, "GATE") for s in GATE_STATES for side in SIDES]
    build += [(f"VTCONT-{side}", "PORTVOL", side, "CONT") for side in SIDES]

    for q, w in product(QS, WS):
        thrs = {}
        for s in GATE_STATES:
            st = states[s]
            mp = max(60, w // 4)
            thrs[(s, "LO")] = st.rolling(w, min_periods=mp).quantile(q)
            thrs[(s, "HI")] = st.rolling(w, min_periods=mp).quantile(1 - q)
        for fam, s_name, side, form in build:
            st = states[s_name]
            thr = thrs[(s_name, side)]
            for depth, cad in product(DEPTHS, CADENCES):
                mult = (gate_mult(st, thr, side, depth, cad, idx) if form == "GATE"
                        else vtcont_mult(st, thr, side, depth, cad, idx))
                m_eff = mult.shift(1).fillna(1.0).loc[ii].values
                fired = m_eff < 1.0
                paths.setdefault((q, w, depth, cad), {})[fam] = (fired, m_eff)
                for g in GROSSES:
                    rb = base[g].loc[ii].values
                    real = {c: apply_eff(rb, m_eff, g, c) for c in RUNGS}
                    rr = real[10]
                    c_, s_, d_ = pack(rr, ii)
                    h1, h2 = halves(rr)
                    oc, os_, od = pack(rr[oos], ii[oos])
                    oh1, oh2 = halves(rr[oos])
                    a4, b4 = keep_paths(c_, s_, d_, h1, h2, bench["bl"], bench["spy"])
                    oa4, ob4 = keep_paths(oc, os_, od, oh1, oh2, bench["bl_oos"], bench["spy_oos"])
                    arms.append(dict(
                        panel=name, family=fam, form=form, side=side, q=q, w=w, depth=depth,
                        cadence=cad, gross=g, rate=float(fired.mean()),
                        gbar=float(m_eff.mean()), gate_turnover=gate_turnover(m_eff),
                        CAGR=c_, Sharpe=s_, MaxDD=d_, H1=h1, H2=h2,
                        IS_Sharpe=fast_sharpe(rr[isw]), OOS_CAGR=oc, OOS_Sharpe=os_,
                        OOS_MaxDD=od, OOS_H1=oh1, OOS_H2=oh2, keep4a=a4, keep4b=b4,
                        oos4a=oa4, oos4b=ob4,
                        **{f"Sharpe_{c}bps": fast_sharpe(real[c]) for c in RUNGS},
                        **{f"CAGR_{c}bps": pack(real[c], ii)[0] for c in RUNGS},
                        **{f"MaxDD_{c}bps": pack(real[c], ii)[2] for c in RUNGS}))

                    if form != "GATE":
                        continue                       # continuous path has no firing-day null
                    mu_r, sg_r = mu_sigma(rr)
                    sh_r, sh_r_is, sh_r_oos = fast_sharpe(rr), fast_sharpe(rr[isw]), fast_sharpe(rr[oos])
                    for kind in KINDS:
                        ex, ml, vl, exi, exo = [], [], [], [], []
                        for sdn in range(NSEED):
                            seed = seed_of(name, fam, q, w, depth, cad, g, kind, sdn)
                            pe = placebo_eff(m_eff, kind, seed, yearkey, volkey)
                            g2 = max(g2, abs(pe.mean() - m_eff.mean()))
                            if sdn == 0:
                                pe2 = placebo_eff(m_eff, kind, seed, yearkey, volkey)
                                g4 = max(g4, float(np.max(np.abs(pe2 - pe))))
                            pr = apply_eff(rb, pe, g, 10)
                            mu_p, sg_p = mu_sigma(pr)
                            e = sh_r - mu_p / sg_p
                            m_leg = (mu_r - mu_p) / sg_r
                            v_leg = mu_p * (sg_p - sg_r) / (sg_r * sg_p)
                            g6 = max(g6, abs(m_leg + v_leg - e))
                            ex.append(e); ml.append(m_leg); vl.append(v_leg)
                            exi.append(sh_r_is - fast_sharpe(pr[isw]))
                            exo.append(sh_r_oos - fast_sharpe(pr[oos]))
                        cells.append(dict(panel=name, family=fam, kind=kind, q=q, w=w,
                                          depth=depth, cadence=cad, gross=g,
                                          excess=float(np.mean(ex)), meanleg=float(np.mean(ml)),
                                          volleg=float(np.mean(vl)), IS_excess=float(np.mean(exi)),
                                          OOS_excess=float(np.mean(exo))))
    log(f"  panel {name}: {len(px.columns)} cols, {len(ii)} days, "
        f"{time.time() - t0:.0f}s")
    return bench, paths, g2, g4, g6


def main():
    t_start = time.time()
    log(f"# Idea 870 - is the CORR-LO excess a VOL TARGET in disguise?  (lane B, {pd.Timestamp.today().date()})")
    log(f"# script: {STEM}.py   10 bps, t+1, weekly book, committed caches only, no network")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    log(f"panels: U56 {panels['U56'].shape}  B136 {panels['B136'].shape}  SMALL {panels['SMALL'].shape}")
    g1, g5 = gates_pre(panels)

    arms, cells, benches, allpaths = [], [], {}, {}
    G2 = G4 = G6 = 0.0
    for nm in ["U56", "B136", "SMALL"]:
        b, p, g2, g4, g6 = run_panel(nm, panels[nm], arms, cells)
        benches[nm] = b; allpaths[nm] = p
        G2, G4, G6 = max(G2, g2), max(G4, g4), max(G6, g6)
    A = pd.DataFrame(arms); C = pd.DataFrame(cells)

    log(f"  G2 placebo mean multiplier == real arm's        max|d| = {G2:.3e}  "
        f"[{'PASS' if G2 < 1e-12 else 'FAIL'}]  (bar 1e-12)")
    log(f"  G4 determinism, every placebo re-seeded          max|d| = {G4:.3e}  "
        f"[{'PASS' if G4 == 0 else 'FAIL'}]  (bar 0)")
    log(f"  G6 MEANLEG + VOLLEG - excess == 0 on every cell  max|d| = {G6:.3e}  "
        f"[{'PASS' if G6 < 1e-10 else 'FAIL'}]  (bar 1e-10)")

    # ---- G3: idea 815's committed CORR medians -------------------------------------------
    like = C[C["panel"].isin(["U56", "B136"])]
    g3ok, g3d = 0, []
    log("  G3 idea 815's committed CORR table, rebuilt here (bar: sign agrees and |d| <= 0.020)")
    log(f"     {'family/kind':<24} {'815':>9} {'here(all)':>10} {'here(U56+B136)':>15} {'|d|':>8}")
    for (fam, kind), v815 in IDEA815.items():
        here = C[(C["family"] == fam) & (C["kind"] == kind)]["excess"].median()
        here_l = like[(like["family"] == fam) & (like["kind"] == kind)]["excess"].median()
        d = abs(here - v815)
        g3d.append(d)
        g3ok += int(np.sign(here) == np.sign(v815) and d <= 0.020)
        log(f"     {fam + '/' + kind:<24} {v815:>+9.4f} {here:>+10.4f} {here_l:>+15.4f} {d:>8.4f}")
    log(f"     G3 {g3ok}/4 cells agree  [{'PASS' if g3ok >= 3 else 'FAIL'}]  "
        f"(median |d| {np.median(g3d):.4f})")
    log(f"  grid: {len(A)} arms ({A['family'].nunique()} families), {len(C)} placebo cells "
        f"x {NSEED} seeds = {len(C) * NSEED:,} placebo evaluations")

    # =================================================================== [1] the decomposition
    log("\n[1] Q2 - THE MEAN/VOL DECOMPOSITION of the BLOCK excess  (exact, no residual)")
    log("    excess = (mu_r - mu_p)/sig_r  +  mu_p*(sig_p - sig_r)/(sig_r*sig_p)")
    log(f"    {'family':<14} {'n':>5} {'excess':>9} {'MEANleg':>9} {'VOLleg':>9} {'VOL share':>10} "
        f"{'|VOL|>|MEAN|':>13}")
    legrows = {}
    for fam in sorted(C["family"].unique()):
        s = C[(C["family"] == fam) & (C["kind"] == "BLOCK")]
        e, m, v = s["excess"].median(), s["meanleg"].median(), s["volleg"].median()
        share = v / e if e != 0 else np.nan
        dom = float((s["volleg"].abs() > s["meanleg"].abs()).mean())
        legrows[fam] = (e, m, v, share, dom)
        log(f"    {fam:<14} {len(s):>5} {e:>+9.4f} {m:>+9.4f} {v:>+9.4f} {share:>10.3f} {dom:>13.3f}")
    e_lo, m_lo, v_lo, share_lo, dom_lo = legrows["CORR-LO"]
    H_LEG = bool(share_lo >= 0.50)
    log(f"    H_LEG (VOL leg >= 50% of CORR-LO's median BLOCK excess): share = {share_lo:.3f} "
        f"-> {'PASS' if H_LEG else 'FAIL'}")

    # ============================================================================= [2] spanning
    log("\n[2] Q3 - DOES A VOL TARGET REPRODUCE CORR-LO's GATE?  (matched q/w/depth/cadence/panel)")
    log(f"    {'comparand':<16} {'n':>5} {'Jaccard':>9} {'rho(path)':>10} {'rate d':>9} {'gbar d':>9}")
    span = {}
    for tgt in ["PORTVOL-LO", "NAMEVOL-LO", "VTCONT-LO", "PORTVOL-HI", "NAMEVOL-HI", "VTCONT-HI"]:
        js, rs, dr, dg = [], [], [], []
        for pan, pmap in allpaths.items():
            for key, fams in pmap.items():
                if "CORR-LO" not in fams or tgt not in fams:
                    continue
                (fa, ma), (fb, mb) = fams["CORR-LO"], fams[tgt]
                js.append(jaccard(fa, fb)); rs.append(pearson(ma, mb))
                dr.append(fb.mean() - fa.mean()); dg.append(mb.mean() - ma.mean())
        span[tgt] = (float(np.nanmedian(js)), float(np.nanmedian(rs)))
        log(f"    {tgt:<16} {len(js):>5} {np.nanmedian(js):>9.3f} {np.nanmedian(rs):>10.3f} "
            f"{np.nanmedian(dr):>+9.3f} {np.nanmedian(dg):>+9.3f}")
    best_tgt = max(span, key=lambda k: span[k][0])
    H_SPAN = bool(span[best_tgt][0] >= 0.50)
    log(f"    H_SPAN (median Jaccard >= 0.50 for some form): best = {best_tgt} at "
        f"{span[best_tgt][0]:.3f} -> {'PASS' if H_SPAN else 'FAIL'}")
    # the identity's own diagnostic: how much of CORR is portfolio vol vs name vol
    log("    variance-identity check - rho(state) on the raw daily states, per panel:")
    for nm, pxp in panels.items():
        core = pxp.drop(columns=["SPY"], errors="ignore")
        cs, pv, nv = state_corr(core), state_portvol(core), state_namevol(core)
        d = pd.concat([cs, pv, nv], axis=1).dropna()
        log(f"      {nm:<6} rho(CORR, PORTVOL) = {spearman(d.iloc[:, 0], d.iloc[:, 1]):+.3f}   "
            f"rho(CORR, NAMEVOL) = {spearman(d.iloc[:, 0], d.iloc[:, 2]):+.3f}   "
            f"rho(PORTVOL, NAMEVOL) = {spearman(d.iloc[:, 1], d.iloc[:, 2]):+.3f}")

    # =============================================================== [3] the vol-regime null
    log("\n[3] Q4 - DOES THE EXCESS SURVIVE A VOL-REGIME-PRESERVING NULL?  median excess, n per cell")
    log(f"    {'family':<14} {'n':>5} {'BLOCK':>9} {'YEARBLOCK':>10} {'VOLBLOCK':>10} "
        f"{'VOLBLOCK-BLOCK':>15} {'cut':>8} {'share>0':>8}")
    nullrows = {}
    for fam in sorted(C["family"].unique()):
        s = C[C["family"] == fam]
        vals = {k: s[s["kind"] == k]["excess"].median() for k in KINDS}
        vb = s[s["kind"] == "VOLBLOCK"]
        cut = 1 - vals["VOLBLOCK"] / vals["BLOCK"] if vals["BLOCK"] != 0 else np.nan
        nullrows[fam] = vals
        log(f"    {fam:<14} {len(vb):>5} {vals['BLOCK']:>+9.4f} {vals['YEARBLOCK']:>+10.4f} "
            f"{vals['VOLBLOCK']:>+10.4f} {vals['VOLBLOCK'] - vals['BLOCK']:>+15.4f} "
            f"{cut:>8.3f} {(vb['excess'] > 0).mean():>8.3f}")
    cut_lo = 1 - nullrows["CORR-LO"]["VOLBLOCK"] / nullrows["CORR-LO"]["BLOCK"]
    H_NULL = bool(cut_lo >= 0.50)
    log(f"    H_NULL (VOLBLOCK cuts CORR-LO's BLOCK excess by >= 50%): cut = {cut_lo:.3f} "
        f"-> {'PASS' if H_NULL else 'FAIL'}")
    log("    per-panel CORR-LO, all three kinds:")
    for nm in ["U56", "B136", "SMALL"]:
        s = C[(C["family"] == "CORR-LO") & (C["panel"] == nm)]
        log(f"      {nm:<6} " + "  ".join(f"{k} {s[s['kind'] == k]['excess'].median():+.4f}" for k in KINDS))

    # ======================================================================== [4] the cost leg
    log("\n[4] Q5 - MATCHED-GROSS PRICING: is a vol target CHEAPER for the same effect?")
    log("    matched on panel/q/w/depth/cadence/gross; gbar d printed so the match is auditable")
    log(f"    {'comparand':<16} {'n':>5} {'d gbar':>8} {'d Sharpe@0':>11} {'@10':>8} {'@25':>8} "
        f"{'d turnover':>11} {'tgt cheaper':>12}")
    key_cols = ["panel", "q", "w", "depth", "cadence", "gross"]
    base_lo = A[A["family"] == "CORR-LO"].set_index(key_cols)
    costrows = {}
    for tgt in ["PORTVOL-LO", "NAMEVOL-LO", "VTCONT-LO", "PORTVOL-HI", "NAMEVOL-HI", "VTCONT-HI"]:
        t = A[A["family"] == tgt].set_index(key_cols)
        j = base_lo.join(t, rsuffix="_t", how="inner")
        ds = {c: (j[f"Sharpe_{c}bps_t"] - j[f"Sharpe_{c}bps"]).median() for c in RUNGS}
        dt = (j["gate_turnover_t"] - j["gate_turnover"]).median()
        wins = all(ds[c] >= 0 for c in RUNGS) and dt < 0
        costrows[tgt] = (ds, dt, wins)
        log(f"    {tgt:<16} {len(j):>5} {(j['gbar_t'] - j['gbar']).median():>+8.4f} "
            f"{ds[0]:>+11.4f} {ds[10]:>+8.4f} {ds[25]:>+8.4f} {dt:>+11.4f} {str(wins):>12}")
    H_COST = bool(costrows[best_tgt][2])
    log(f"    H_COST (best-spanning form {best_tgt} >= CORR-LO at ALL rungs AND lower turnover) "
        f"-> {'PASS' if H_COST else 'FAIL'}")
    log("    CORR-LO's own cost sensitivity, median over its arms (the 'worse cost' claim, direct):")
    lo = A[A["family"] == "CORR-LO"]
    for tgt in ["CORR-LO", best_tgt]:
        s = A[A["family"] == tgt]
        log(f"      {tgt:<14} gate turnover {s['gate_turnover'].median():.4f}/yr   Sharpe "
            + "  ".join(f"@{c}bps {s[f'Sharpe_{c}bps'].median():.3f}" for c in RUNGS)
            + f"   decay 0->25 {s['Sharpe_0bps'].median() - s['Sharpe_25bps'].median():+.4f}")

    # ====================================================================== [5] rule 8 + books
    log("\n[5] Q6 - RULE 8.  (a) does the EXCESS walk forward?  rho(IS excess, OOS excess), n=arms")
    log(f"    {'family':<14} " + "".join(f"{k:>13}" for k in KINDS))
    wf = {}
    for fam in sorted(C["family"].unique()):
        row = []
        for k in KINDS:
            s = C[(C["family"] == fam) & (C["kind"] == k)]
            row.append(spearman(s["IS_excess"], s["OOS_excess"]))
        wf[fam] = dict(zip(KINDS, row))
        log(f"    {fam:<14} " + "".join(f"{v:>+13.3f}" for v in row))
    H_WF = bool(wf["CORR-LO"]["BLOCK"] >= 0.30 and wf[best_tgt]["BLOCK"] >= 0.30) \
        if best_tgt in wf else False
    log(f"    idea 815 committed CORR-LO BLOCK rho = {IDEA815_WF['CORR-LO-BLOCK']:+.3f}, "
        f"here {wf['CORR-LO']['BLOCK']:+.3f}")
    log(f"    H_WF (CORR-LO AND {best_tgt} both rho >= +0.30 under BLOCK) -> "
        f"{'PASS' if H_WF else 'FAIL'}"
        + ("" if best_tgt in wf else f"  [{best_tgt} is continuous - no firing-day null]"))

    log("\n    (b) THE BOOKS.  Comparands @10 bps, weekly, t+1, per panel:")
    for nm in ["U56", "B136", "SMALL"]:
        b = benches[nm]
        log(f"      {nm:<6} SPY {b['spy']['c']:.2%}/{b['spy']['s']:.3f}/{b['spy']['dd']:.2%} "
            f"(H {b['spy']['h1']:.3f}/{b['spy']['h2']:.3f}; OOS {b['spy_oos']['c']:.2%}/"
            f"{b['spy_oos']['s']:.3f}/{b['spy_oos']['dd']:.2%})   "
            f"RULES v2 {b['bl']['c']:.2%}/{b['bl']['s']:.3f}/{b['bl']['dd']:.2%} "
            f"(OOS {b['bl_oos']['c']:.2%}/{b['bl_oos']['s']:.3f}/{b['bl_oos']['dd']:.2%})")

    log("\n    full-sample KEEP census over ALL grid points (nothing selected):")
    log(f"    {'family':<14} {'arms':>6} {'4a':>5} {'4b':>5} {'med Sharpe':>11} {'med CAGR':>10} "
        f"{'best OOS Sh':>12} {'OOS 4a':>7} {'OOS 4b':>7}")
    for fam in sorted(A["family"].unique()):
        s = A[A["family"] == fam]
        log(f"    {fam:<14} {len(s):>6} {int(s['keep4a'].sum()):>5} {int(s['keep4b'].sum()):>5} "
            f"{s['Sharpe'].median():>11.3f} {s['CAGR'].median():>10.2%} "
            f"{s['OOS_Sharpe'].max():>12.3f} {int(s['oos4a'].sum()):>7} {int(s['oos4b'].sum()):>7}")
    log(f"    TOTAL          {len(A):>6} {int(A['keep4a'].sum()):>5} {int(A['keep4b'].sum()):>5}")

    log("\n    cost ladder over ALL arms, per rung (parameter 2 - every rung reported):")
    for c in RUNGS:
        log(f"      {c:>2} bps  median Sharpe {A[f'Sharpe_{c}bps'].median():.3f}   "
            f"median CAGR {A[f'CAGR_{c}bps'].median():.2%}   "
            f"median MaxDD {A[f'MaxDD_{c}bps'].median():.2%}   "
            f"CORR-LO median Sharpe {lo[f'Sharpe_{c}bps'].median():.3f}")

    log("\n    (c) IS-ONLY SELECTOR (highest 2009-2016 Sharpe per panel x family), OOS READ ONCE:")
    log(f"    {'panel':<6} {'family':<14} {'q':>5} {'w':>5} {'dep':>5} {'cad':>4} {'g':>5} "
        f"{'OOS CAGR':>9} {'OOS Sh':>7} {'OOS DD':>8} {'OOS H1/H2':>13} {'4a':>4} {'4b':>4}")
    picks = []
    for nm in ["U56", "B136", "SMALL"]:
        for fam in sorted(A["family"].unique()):
            s = A[(A["panel"] == nm) & (A["family"] == fam)]
            if s.empty:
                continue
            p = s.loc[s["IS_Sharpe"].idxmax()]
            picks.append(p)
            log(f"    {nm:<6} {fam:<14} {p['q']:>5.2f} {int(p['w']):>5} {p['depth']:>5.2f} "
                f"{p['cadence']:>4} {p['gross']:>5.2f} {p['OOS_CAGR']:>9.2%} {p['OOS_Sharpe']:>7.3f} "
                f"{p['OOS_MaxDD']:>8.2%} {p['OOS_H1']:>6.3f}/{p['OOS_H2']:<6.3f} "
                f"{str(bool(p['oos4a'])):>4} {str(bool(p['oos4b'])):>4}")
    P = pd.DataFrame(picks)
    log(f"    rule-8 picks: {len(P)}   OOS 4a {int(P['oos4a'].sum())}   OOS 4b {int(P['oos4b'].sum())}"
        f"   CORR-LO picks passing OOS 4b: {int(P[P['family'] == 'CORR-LO']['oos4b'].sum())} of "
        f"{len(P[P['family'] == 'CORR-LO'])}")

    # ------------------------------------------------------------------------------- verdict
    log("\n[6] PRE-REGISTERED BARS, ALL FIVE")
    for nm_, v in [("H_LEG", H_LEG), ("H_SPAN", H_SPAN), ("H_NULL", H_NULL),
                   ("H_COST", H_COST), ("H_WF", H_WF)]:
        log(f"    {nm_:<8} {'PASS' if v else 'FAIL'}")

    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    C.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    P.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    log(f"\nwrote {STEM}.arms.csv ({len(A)}), .cells.csv ({len(C)}), .picks.csv ({len(P)})")
    log(f"total {time.time() - t_start:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

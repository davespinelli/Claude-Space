#!/usr/bin/env python3
"""Idea 901 - "does-the-BLOCK-null-MASK-every-LOW-TAIL-gate-in-the-record" (lane B, 2026-09-15).

The finding this run exists to generalise
------------------------------------------
Idea 870 (lane B, yesterday's run) built VOLBLOCK - a rate- and run-length-matched circular
shift applied INDEPENDENTLY WITHIN EACH REALISED-VOL TERCILE of the ungated equal-weight book -
expecting it to ERASE CORR-LO's placebo excess the way idea 815's EPISODEFIX erased the other
four families'.  It did the opposite:

    CORR-LO median excess   BLOCK +0.0298  ->  VOLBLOCK +0.0792   (2.7x, on 99.5% of arms)

The mechanism it proposed: BLOCK is free to roll a gate's firing days ANYWHERE on the calendar,
including into high-vol days.  De-grossing on a high-vol day pays for free (the book's variance
is the denominator of the Sharpe the placebo is scored on), so a BLOCK placebo built from a
LOW-tail gate systematically LANDS IN A BETTER VOL REGIME THAN THE REAL ARM EVER SITS IN.  The
placebo therefore scores too high and the published excess - real minus placebo - is TOO SMALL.

If that mechanism is right it is not a CORR fact, and it is not a fact about one null.  It is a
SIGNED bias that every LOW-tail gate in the record inherits, and the same argument run backwards
says HIGH-tail gates must be biased the OTHER way: their real firing days are already the
high-vol days, so a BLOCK placebo rolls them into calmer regimes, scores too LOW, and the
published excess is TOO BIG.  That is the prediction this run puts at risk on the whole record.

What is priced here
-------------------
    (A) RE-PRICE.  Every LOW-tail gate family the record actually uses, rebuilt on committed
        caches, priced under BLOCK and under VOLBLOCK at three stratum counts, on the full
        602/606/815 grid (q x w x depth x cadence x gross x panel).  Both sides always.
    (B) CENSUS.  Every committed per-arm placebo-differenced LOW-tail number in the repo that
        NAMES ITS NULL, harvested from the committed CSVs and re-priced against VOLBLOCK on
        its own key, so the question "how many published excesses are understated" is answered
        by counting them, not by extrapolating from CORR-LO.
    (C) CAPITAL.  PROTOCOL rule 8 walk-forward on the re-priced LOW-tail book, both KEEP paths,
        OOS CAGR/Sharpe/MaxDD against the live baseline and SPY - because a bigger excess that
        still buys no capital is a measurement result, not a book.

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (MASK)   Is the BLOCK-to-VOLBLOCK uplift positive for EVERY low-tail family, or is
                CORR-LO special?
    Q2 (SIGN)   Is the bias SIGNED by tail - up on LO, down on HI - as the mechanism requires?
                A uniform uplift on both sides would falsify the mechanism and leave the
                2.7x as something else.
    Q3 (STRAT)  Is the uplift a tercile artefact?  Re-run at 2 / 3 / 5 strata.
    Q4 (COUNT)  Of the record's committed LO-tail placebo numbers that name their null, how
                many are understated, and how many restate past a 20% materiality bar?
    Q5 (CAPITAL) Does any re-priced LO arm clear 4a or 4b, in sample or out (rule 8)?

Pre-registered hypotheses and bars (fixed before any number below section [0] was read)
    H_MASK   The median (VOLBLOCK3 - BLOCK) excess is > 0 for ALL LO families, not just CORR-LO.
             PASS = the masking is a property of the LOW TAIL, not of correlation.
    H_SIGN   Pooled over families, median uplift on LO arms > 0 AND median uplift on HI arms < 0.
             PASS = BLOCK carries a SIGNED, tail-keyed bias.  A same-sign result on both tails
             FAILS and sends the 2.7x back to being unexplained.
    H_STRAT  The SIGN of the per-family-per-panel median uplift is the same at k = 2, 3 and 5
             on >= 90% of family x panel cells.  PASS = not an artefact of the tercile cut.
    H_COUNT  >= 90% of the harvested committed LO rows in the NARROW claim set (kind == BLOCK)
             are understated, i.e. the VOLBLOCK re-price is strictly larger than the published
             number on the same arm key.
    H_CAP    At least one LO arm's rule-8 IS pick clears OOS 4b.  (Idea 870 reported 0 of 432
             on the four LO families it saw; this is the bar that says re-pricing changed
             something that matters for capital.  It is expected to FAIL and is stated anyway.)
  A FAIL on any of these is a result and is printed as one.  Nothing is re-specified after a bar
  is read.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. claim set   NARROW (kind == BLOCK, the null idea 901 names)
                   SHIFT  (every BLOCK-family circular-shift null in the record: BLOCK, BLOCK2,
                           BLOCKPOST, BLOCKEP, BLOCKYEAR, YEARBLOCK, SHIFT10/21/126)
                   ALL    (every committed placebo kind on LO rows, RAND and the run-length
                           families included - the widest defensible reading)
    2. stratum count  k = 2 / 3 / 5 realised-vol strata for VOLBLOCK.
    ALL 3 x 3 grid points reported.  Every reported axis below is swept, never selected on.

Reported axes, NEVER tuned or selected on (inherited from ideas 602/606/815 verbatim)
    level q 0.07 / 0.12 / 0.17     w 252 / 504 / 1008 / 2016     depth 0.25 / 0.50 / 1.00
    cadence D / W                  gross 0.75 / 1.00             panel U56 / B136 / SMALL
    cost rung 0 / 10 / 25 bps      SIDE (LO / HI) - both always reported, never selected on.

States: the record's four (BREADTH, VOL20, DISP, CORR from ideas 606/815) plus PORTVOL (idea
870).  NAMEVOL is idea 870's name for VOL20 and is NOT carried twice; the identity is checked
in section [0] instead.

The placebo kinds
    BLOCK       circular shift of the whole effective path - exact rate AND exact run-length
                multiset, no calendar alignment.                          (ideas 606 / 815)
    YEARBLOCK   circular shift independently within each calendar year.   (idea 815, carried
                for continuity with the committed record)
    VOLBLOCKk   circular shift independently within each of k realised-vol strata of the ungated
                equal-weight book (k = 2, 3, 5).  Exact per-stratum firing count, near-exact run
                lengths, every de-grossed day stays in the vol regime it was in.  k = 3 is idea
                870's VOLBLOCK exactly.  k = 1 IS BLOCK by construction and is used as gate G6.
    Strata are full-sample quantile cuts of a state the null never trades; like idea 815's
    declared episodes they are a MEASUREMENT DEVICE, not a tradeable path.  Stated, not hidden.

Reproduction gates (section [0], printed before any new number is read)
    G1  a never-firing multiplier path reproduces the ungated book exactly.
    G2  THE TWIN CANCELS: every placebo kind's mean effective multiplier equals the real arm's.
    G3  idea 815's committed CORR BLOCK/YEARBLOCK medians and idea 870's committed CORR-LO
        VOLBLOCK median, both rebuilt here from the committed CSVs, not from prose.
    G4  determinism: every placebo recomputed from its md5 seed, max |d| must be 0.
    G5  the fast Sharpe used on the placebo cells equals engine.metrics()["Sharpe"].
    G6  VOLBLOCK at k = 1 is BLOCK bit-for-bit at the same seed.
    G7  VOL20 and idea 870's NAMEVOL are the same state (max |d| = 0).

Data: committed caches only, no network, never yfinance.
SURVIVORSHIP: all three panels are current-constituent lists (the small panel additionally
drops every ticker with max_1d_move >= 1.0 per data/small_meta.csv), so CAGR and drawdown
LEVELS are optimistic throughout; the placebo DIFFERENCING and the BLOCK-vs-VOLBLOCK contrast
are the durable part.
PANEL DRIFT: the record's small panel is committed under three names (SMALL439, SMALL663,
SMALL) as the screen grew.  The census normalises them to SMALL and reports the U56+B136-only
count beside the pooled one, because only those two panels are byte-stable across the record.

Deterministic (all placebo seeds md5-derived), standalone.  Modifies nothing.
"""
import glob
import hashlib
import re
import sys
import time
import warnings
from itertools import product
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

warnings.filterwarnings("ignore")

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
STRATA = [2, 3, 5]                       # parameter 2
KINDS = ["BLOCK", "YEARBLOCK"] + [f"VOLBLOCK{k}" for k in STRATA]
PANELS = ["U56", "B136", "SMALL"]

GATE_STATES = ["BREADTH", "VOL20", "DISP", "CORR", "PORTVOL"]
SIDES = ("LO", "HI")

# parameter 1: the claim set.  Kind names as the record spells them.
SHIFT_KINDS = {"BLOCK", "BLOCK2", "BLOCKPOST", "BLOCKEP", "BLOCKYEAR", "YEARBLOCK",
               "SHIFT10", "SHIFT21", "SHIFT126"}
CLAIMSETS = ["NARROW", "SHIFT", "ALL"]
MATERIAL = 0.20                          # restatement bar for Q4, fixed in advance

# committed numbers used as reproduction gates, read from the committed CSVs where possible
IDEA815_FILE = OUT / "2026-09-15_is-the-CORR-LO-POSITIVE-EXCESS-a-DE-GROSSING-artefact_cloud.excess.csv"
IDEA870_FILE = OUT / "2026-09-15_is-the-CORR-LO-excess-a-VOL-TARGET-in-disguise_B.cells.csv"


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
    """Average NAME vol.  Idea 870 calls the identical object NAMEVOL; G7 checks that."""
    return (px.pct_change().rolling(SMOOTH).std() * np.sqrt(252)).mean(axis=1)


def state_disp(px):
    return px.pct_change().std(axis=1).rolling(SMOOTH).mean()


def state_portvol(px):
    """Realised vol of the equal-weight book - the state VOLBLOCK stratifies on."""
    return px.pct_change().mean(axis=1).rolling(SMOOTH).std() * np.sqrt(252)


def state_corr(px):
    """20d average pairwise correlation, equal-weight index-vs-name variance identity."""
    rt = px.pct_change()
    sig = rt.rolling(SMOOTH).std()
    s_idx = rt.mean(axis=1).rolling(SMOOTH).std()
    n = sig.notna().sum(axis=1).replace(0, np.nan)
    sbar, s2bar = sig.mean(axis=1), (sig ** 2).mean(axis=1)
    return ((s_idx ** 2 - s2bar / n) / (sbar ** 2 - s2bar / n).replace(0, np.nan)).clip(-1, 1)


STATE_FN = {"BREADTH": state_breadth, "VOL20": state_vol20, "DISP": state_disp,
            "CORR": state_corr, "PORTVOL": state_portvol}


def gate_mult(st, thr, side, depth, cadence, idx):
    """Fire (de-gross to 1-depth) when the state is in its named tail; 1.0 before the rolling
    threshold exists.  LO fires on st < thr, HI on st > thr.  idea 606/815 verbatim."""
    fire = ((st < thr) if side == "LO" else (st > thr)) & st.notna() & thr.notna()
    m = pd.Series(1.0, index=idx).where(~fire, 1.0 - depth)
    if cadence == "W":
        m = m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)
    return m


def apply_eff(r_base, m_eff, gross, cost_bps):
    """Apply an ALREADY-EFFECTIVE (t+1-aligned) multiplier path with idea 399's switch cost."""
    switch = np.abs(np.diff(m_eff, prepend=m_eff[0]))
    return m_eff * r_base - switch * gross * cost_bps / 1e4


def gate_turnover(m_eff):
    return float(np.abs(np.diff(m_eff, prepend=m_eff[0])).sum() * 252 / len(m_eff))


def seed_of(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def placebo_eff(m_eff, kind, seed, yearkey, volkeys):
    """Rate-matched, information-free twin of the EFFECTIVE multiplier path (numpy).
    Segment-wise np.roll preserves each segment's multiset exactly, so the per-segment firing
    count is EXACT and the pooled mean multiplier is exact for every kind."""
    v = np.asarray(m_eff, float)
    if (v < 1.0).sum() == 0:
        return v.copy()
    rng = np.random.default_rng(seed)
    if kind == "BLOCK":
        return np.roll(v, int(rng.integers(1, len(v))))
    segs = yearkey if kind == "YEARBLOCK" else volkeys[int(kind.replace("VOLBLOCK", ""))]
    out = v.copy()
    for key in np.unique(segs):
        sel = segs == key
        seg = v[sel]
        if len(seg) > 1:
            out[sel] = np.roll(seg, int(rng.integers(1, len(seg))))
    return out


def vol_strata(pv, k):
    """k full-sample quantile strata of the realised portfolio vol.  k = 1 -> a single stratum,
    which makes VOLBLOCK1 identical to BLOCK (gate G6)."""
    if k <= 1:
        return np.zeros(len(pv), dtype=int)
    cuts = pv.quantile([i / k for i in range(1, k)]).values
    return np.digitize(pv.fillna(pv.median()).values, cuts)


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

    # G6 - VOLBLOCK1 is BLOCK, bit for bit, at the same seed
    rng = np.random.default_rng(7)
    fake = np.where(rng.random(len(r_base)) < 0.12, 0.5, 1.0)
    pv = state_portvol(px).loc[r_base.index]
    vk = {1: vol_strata(pv, 1)}
    a = placebo_eff(fake, "BLOCK", 12345, r_base.index.year.values, vk)
    b = placebo_eff(fake, "VOLBLOCK1", 12345, r_base.index.year.values, vk)
    g6 = float(np.max(np.abs(a - b)))
    log(f"  G6 VOLBLOCK at k=1 == BLOCK at the same seed     max|d| = {g6:.3e}  "
        f"[{'PASS' if g6 == 0 else 'FAIL'}]  (bar 0)")

    # G7 - VOL20 is idea 870's NAMEVOL
    namevol = (px.pct_change().rolling(SMOOTH).std() * np.sqrt(252)).mean(axis=1)
    g7 = float(np.nanmax(np.abs(state_vol20(px) - namevol)))
    log(f"  G7 VOL20 == idea 870's NAMEVOL                   max|d| = {g7:.3e}  "
        f"[{'PASS' if g7 == 0 else 'FAIL'}]  (bar 0; NAMEVOL is therefore not carried twice)")
    return g1, g5, g6, g7


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
    oos = np.asarray(ii >= pd.Timestamp(SPLIT))
    isw = ~oos

    pv = states["PORTVOL"].loc[ii]
    volkeys = {k: vol_strata(pv, k) for k in STRATA}
    volkeys[1] = vol_strata(pv, 1)
    # percentile rank of realised portfolio vol on every day - the axis section [2b] tests.
    # A BLOCK placebo has mean firing-day percentile 0.500 by construction.
    pvpct = states["PORTVOL"].rank(pct=True).loc[ii].values

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

    g2 = g4 = 0.0
    for q, w in product(QS, WS):
        thrs = {}
        for s in GATE_STATES:
            st = states[s]
            mp = max(60, w // 4)
            thrs[(s, "LO")] = st.rolling(w, min_periods=mp).quantile(q)
            thrs[(s, "HI")] = st.rolling(w, min_periods=mp).quantile(1 - q)
        for s_name, side in product(GATE_STATES, SIDES):
            fam = f"{s_name}-{side}"
            st, thr = states[s_name], thrs[(s_name, side)]
            for depth, cad in product(DEPTHS, CADENCES):
                mult = gate_mult(st, thr, side, depth, cad, idx)
                m_eff = mult.shift(1).fillna(1.0).loc[ii].values
                fired = m_eff < 1.0
                fvp = float(np.nanmean(pvpct[fired])) if fired.sum() else np.nan
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
                        panel=name, family=fam, state=s_name, side=side, q=q, w=w, depth=depth,
                        cadence=cad, gross=g, rate=float(fired.mean()), fire_volpct=fvp,
                        gbar=float(m_eff.mean()), gate_turnover=gate_turnover(m_eff),
                        CAGR=c_, Sharpe=s_, MaxDD=d_, H1=h1, H2=h2,
                        IS_Sharpe=fast_sharpe(rr[isw]), OOS_CAGR=oc, OOS_Sharpe=os_,
                        OOS_MaxDD=od, OOS_H1=oh1, OOS_H2=oh2, keep4a=a4, keep4b=b4,
                        oos4a=oa4, oos4b=ob4,
                        **{f"Sharpe_{c}bps": fast_sharpe(real[c]) for c in RUNGS},
                        **{f"CAGR_{c}bps": pack(real[c], ii)[0] for c in RUNGS},
                        **{f"MaxDD_{c}bps": pack(real[c], ii)[2] for c in RUNGS}))

                    sh_r = {c: fast_sharpe(real[c]) for c in RUNGS}
                    sh_is, sh_oos = fast_sharpe(rr[isw]), fast_sharpe(rr[oos])
                    for kind in KINDS:
                        acc = {f"excess_{c}bps": [] for c in RUNGS}
                        exi, exo = [], []
                        for sdn in range(NSEED):
                            seed = seed_of(name, fam, q, w, depth, cad, g, kind, sdn)
                            pe = placebo_eff(m_eff, kind, seed, yearkey, volkeys)
                            g2 = max(g2, abs(pe.mean() - m_eff.mean()))
                            if sdn == 0:
                                g4 = max(g4, float(np.max(np.abs(
                                    placebo_eff(m_eff, kind, seed, yearkey, volkeys) - pe))))
                            for c in RUNGS:
                                acc[f"excess_{c}bps"].append(
                                    sh_r[c] - fast_sharpe(apply_eff(rb, pe, g, c)))
                            pr = apply_eff(rb, pe, g, 10)
                            exi.append(sh_is - fast_sharpe(pr[isw]))
                            exo.append(sh_oos - fast_sharpe(pr[oos]))
                        cells.append(dict(panel=name, family=fam, state=s_name, side=side,
                                          kind=kind, q=q, w=w, depth=depth, cadence=cad, gross=g,
                                          rate=float(fired.mean()),
                                          **{k_: float(np.mean(v)) for k_, v in acc.items()},
                                          excess_IS=float(np.mean(exi)),
                                          excess_OOS=float(np.mean(exo))))
    log(f"  panel {name}: {len(px.columns)} cols, {len(ii)} days, {time.time() - t0:.0f}s")
    return bench, g2, g4


# ============================================================================ census harvester
KEYCOLS = ["panel", "family", "q", "w", "depth", "cadence", "gross"]


def norm_panel(p):
    p = str(p)
    return "SMALL" if p.upper().startswith("SMALL") else p


def harvest():
    """Every committed per-arm placebo-differenced LOW-tail number in research/backtests that
    NAMES ITS NULL.  A file qualifies only if it carries the arm key AND either a 'kind' column
    or kind-suffixed excess columns; a bare 'dSharpe'/'excess' with no named null is SKIPPED
    (matched-gross twin differences live in those columns too, and are not placebo numbers)."""
    rows, skipped, used = [], [], []
    files = sorted(glob.glob(str(OUT / "*.csv")) + glob.glob(str(OUT / "*.csv.gz")))
    for f in files:
        base = Path(f).name
        if base.startswith(STEM):
            continue            # never harvest this run's own output - the census must not
        try:                    # depend on whether the script has been run before
            head = pd.read_csv(f, nrows=0).columns.tolist()
        except Exception:
            continue
        if not ({"w", "depth", "cadence", "gross"} <= set(head)):
            continue
        if not (("q" in head) or ("level" in head)):
            continue
        if not (("side" in head) or ("family" in head)):
            continue
        try:
            d = pd.read_csv(f)
        except Exception:
            continue
        if "level" in d.columns and "q" not in d.columns:
            d = d.rename(columns={"level": "q"})
        if "family" not in d.columns and {"state", "side"} <= set(d.columns):
            d["family"] = d["state"].astype(str) + "-" + d["side"].astype(str)
        lo = d[d["family"].astype(str).str.endswith("-LO")].copy()
        if lo.empty:
            continue
        if "rung" in lo.columns and 10 in set(lo["rung"].unique()):
            lo = lo[lo["rung"] == 10]
        lo["panel"] = lo["panel"].map(norm_panel) if "panel" in lo.columns else "U56"

        # a file carrying a 'seed' column stores the individual draws, not the published
        # number; the published number is the seed MEAN, so collapse to it first.
        seedwise = "seed" in lo.columns

        got = []
        if "kind" in lo.columns:
            col = next((c for c in ["excess_10bps", "excess", "dSharpe"] if c in lo.columns), None)
            if col:
                t = lo[KEYCOLS + ["kind", col]].rename(columns={col: "pub"})
                if seedwise:
                    t = t.groupby(KEYCOLS + ["kind"], as_index=False)["pub"].mean()
                got.append((t, col + (" (seed mean)" if seedwise else "")))
        else:
            for c in lo.columns:
                m = re.fullmatch(r"(dSharpe|excess_vs|excess)_([A-Z0-9_]+)", c)
                if not m or m.group(2) in {"IS", "OOS"}:
                    continue
                t = lo[KEYCOLS + [c]].rename(columns={c: "pub"})
                t["kind"] = m.group(2)
                if seedwise:
                    t = t.groupby(KEYCOLS + ["kind"], as_index=False)["pub"].mean()
                got.append((t, c + (" (seed mean)" if seedwise else "")))
        if not got:
            skipped.append(base)
            continue
        n = 0
        for t, col in got:
            t = t.dropna(subset=["pub"])
            t["file"] = base
            t["col"] = col
            rows.append(t)
            n += len(t)
        used.append((base, n))
    H = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    return H, used, skipped


def main():
    t_start = time.time()
    log(f"# Idea 901 - does the BLOCK null MASK every LOW-TAIL gate in the record?  "
        f"(lane B, {pd.Timestamp.today().date()})")
    log(f"# script: {STEM}.py   10 bps, t+1, weekly book, committed caches only, no network")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    log(f"panels: U56 {panels['U56'].shape}  B136 {panels['B136'].shape}  SMALL {panels['SMALL'].shape}")
    g1, g5, g6, g7 = gates_pre(panels)

    arms, cells, benches = [], [], {}
    G2 = G4 = 0.0
    for nm in PANELS:
        b, g2, g4 = run_panel(nm, panels[nm], arms, cells)
        benches[nm] = b
        G2, G4 = max(G2, g2), max(G4, g4)
    A = pd.DataFrame(arms)
    C = pd.DataFrame(cells)
    C["excess"] = C["excess_10bps"]

    log(f"  G2 placebo mean multiplier == real arm's        max|d| = {G2:.3e}  "
        f"[{'PASS' if G2 < 1e-12 else 'FAIL'}]  (bar 1e-12)")
    log(f"  G4 determinism, every placebo re-seeded          max|d| = {G4:.3e}  "
        f"[{'PASS' if G4 == 0 else 'FAIL'}]  (bar 0)")

    # ---- G3: the committed numbers this run must reproduce, read from committed CSVs --------
    log("  G3 committed medians rebuilt here (bar: sign agrees and |d| <= 0.020)")
    log(f"     {'source / family / kind':<44} {'committed':>10} {'here':>10} {'|d|':>8}")
    g3ok, g3n, g3d = 0, 0, []
    ref = []
    if IDEA815_FILE.exists():
        c815 = pd.read_csv(IDEA815_FILE)
        for fam in ["CORR-LO", "CORR-HI"]:
            for k in ["BLOCK", "YEARBLOCK"]:
                s = c815[(c815["family"] == fam) & (c815["kind"] == k)]
                if len(s):
                    ref.append((f"815 {fam}/{k}", fam, k, float(s["excess"].median())))
    if IDEA870_FILE.exists():
        c870 = pd.read_csv(IDEA870_FILE)
        for fam in ["CORR-LO"]:
            for k, here_k in [("BLOCK", "BLOCK"), ("VOLBLOCK", "VOLBLOCK3")]:
                s = c870[(c870["family"] == fam) & (c870["kind"] == k)]
                if len(s):
                    ref.append((f"870 {fam}/{k}", fam, here_k, float(s["excess"].median())))
    for label, fam, k, v in ref:
        here = C[(C["family"] == fam) & (C["kind"] == k)]["excess"].median()
        d = abs(here - v)
        g3d.append(d)
        g3n += 1
        g3ok += int(np.sign(here) == np.sign(v) and d <= 0.020)
        log(f"     {label + '  -> here ' + k:<44} {v:>+10.4f} {here:>+10.4f} {d:>8.4f}")
    log(f"     G3 {g3ok}/{g3n} cells agree  [{'PASS' if g3n and g3ok >= g3n - 1 else 'FAIL'}]  "
        f"(median |d| {np.median(g3d) if g3d else float('nan'):.4f})")
    log(f"  grid: {len(A)} arms ({A['family'].nunique()} families, {len(PANELS)} panels), "
        f"{len(C)} placebo cells x {NSEED} seeds = {len(C) * NSEED:,} placebo evaluations")

    # ================================================================= [1] Q1/Q3 - the uplift
    log("\n[1] Q1 (MASK) + Q3 (STRAT) - median placebo excess by family and null kind @10 bps")
    log("    uplift = VOLBLOCKk - BLOCK.  positive uplift = the published BLOCK number is TOO SMALL")
    log(f"    {'family':<13} {'n/kind':>6} {'BLOCK':>9} {'YEARBLK':>9} "
        + "".join(f"{'VB' + str(k):>9}" for k in STRATA)
        + "".join(f"{'upl' + str(k):>9}" for k in STRATA) + f"{'share>0 (k=3)':>15}")
    upl = {}
    for side in ["LO", "HI"]:
        for fam in sorted(C[C["side"] == side]["family"].unique()):
            s = C[C["family"] == fam]
            med = {k: s[s["kind"] == k]["excess"].median() for k in KINDS}
            u = {k: med[f"VOLBLOCK{k}"] - med["BLOCK"] for k in STRATA}
            upl[fam] = u
            b = s[s["kind"] == "BLOCK"].set_index(KEYCOLS)["excess"]
            v3 = s[s["kind"] == "VOLBLOCK3"].set_index(KEYCOLS)["excess"]
            j = pd.concat([b.rename("b"), v3.rename("v")], axis=1).dropna()
            log(f"    {fam:<13} {len(s[s['kind'] == 'BLOCK']):>6} {med['BLOCK']:>+9.4f} "
                f"{med['YEARBLOCK']:>+9.4f}"
                + "".join(f"{med['VOLBLOCK' + str(k)]:>+9.4f}" for k in STRATA)
                + "".join(f"{u[k]:>+9.4f}" for k in STRATA)
                + f"{(j['v'] > j['b']).mean():>15.3f}")
        log("    " + "-" * 100)
    lo_fams = [f for f in upl if f.endswith("-LO")]
    hi_fams = [f for f in upl if f.endswith("-HI")]
    H_MASK = all(upl[f][3] > 0 for f in lo_fams)
    log(f"    H_MASK (median VOLBLOCK3 - BLOCK > 0 for ALL {len(lo_fams)} LO families): "
        f"{sum(upl[f][3] > 0 for f in lo_fams)}/{len(lo_fams)} -> {'PASS' if H_MASK else 'FAIL'}")

    # per-panel, per-stratum sign stability (H_STRAT)
    sign_rows = []
    for fam in sorted(C["family"].unique()):
        for pan in PANELS:
            s = C[(C["family"] == fam) & (C["panel"] == pan)]
            b = s[s["kind"] == "BLOCK"]["excess"].median()
            sg = [np.sign(s[s["kind"] == f"VOLBLOCK{k}"]["excess"].median() - b) for k in STRATA]
            sign_rows.append(dict(family=fam, panel=pan, side=fam.split("-")[-1],
                                  **{f"s{k}": sg[i] for i, k in enumerate(STRATA)},
                                  stable=len(set(sg)) == 1))
    S = pd.DataFrame(sign_rows)
    stab = float(S["stable"].mean())
    H_STRAT = stab >= 0.90
    log(f"    H_STRAT (sign of the uplift identical at k=2/3/5 on >= 90% of family x panel "
        f"cells): {stab:.3f} on {len(S)} cells -> {'PASS' if H_STRAT else 'FAIL'}")
    log(f"      unstable cells: "
        + (", ".join(f"{r.family}/{r.panel}" for r in S[~S['stable']].itertuples()) or "none"))

    # ===================================================================== [2] Q2 - the sign
    log("\n[2] Q2 (SIGN) - is the BLOCK bias SIGNED BY TAIL?  per-arm uplift, pooled over families")
    log(f"    {'side':<6} {'arms':>7} " + "".join(f"{'med upl k=' + str(k):>14}" for k in STRATA)
        + f"{'share>0 (k=3)':>15}")
    sidestat = {}
    for side in ["LO", "HI"]:
        s = C[C["side"] == side]
        b = s[s["kind"] == "BLOCK"].set_index(KEYCOLS)["excess"]
        meds, sh = [], None
        for k in STRATA:
            v = s[s["kind"] == f"VOLBLOCK{k}"].set_index(KEYCOLS)["excess"]
            j = pd.concat([b.rename("b"), v.rename("v")], axis=1).dropna()
            meds.append(float((j["v"] - j["b"]).median()))
            if k == 3:
                sh = float((j["v"] > j["b"]).mean())
                n = len(j)
        sidestat[side] = (meds, sh)
        log(f"    {side:<6} {n:>7} " + "".join(f"{m:>+14.4f}" for m in meds) + f"{sh:>15.3f}")
    H_SIGN = sidestat["LO"][0][1] > 0 > sidestat["HI"][0][1]
    log(f"    H_SIGN (median uplift LO > 0 AND HI < 0 at k=3): "
        f"LO {sidestat['LO'][0][1]:+.4f}, HI {sidestat['HI'][0][1]:+.4f} -> "
        f"{'PASS' if H_SIGN else 'FAIL'}")
    # ------------------------------------------------------------ [2b] the explanatory axis
    log("\n[2b] POST-HOC (not pre-registered) - WHAT THE UPLIFT IS ACTUALLY KEYED TO.")
    log("    H_MASK and H_SIGN are both stated on the LO/HI label.  The mechanism is not about")
    log("    the label: it is about WHERE ON THE VOL DISTRIBUTION a gate's firing days sit.  A")
    log("    BLOCK placebo lands at percentile 0.500 by construction, so it should score TOO")
    log("    HIGH (excess understated) for a gate firing below 0.500 and TOO LOW (excess")
    log("    overstated) for one firing above it.  fire_volpct is measured per arm, uplift is")
    log("    that same arm's VOLBLOCK3 - BLOCK.  This table is a DIAGNOSTIC of a bar already")
    log("    read, not a new bar.")
    upl_arm = (C[C["kind"] == "VOLBLOCK3"].set_index(KEYCOLS)["excess"]
               - C[C["kind"] == "BLOCK"].set_index(KEYCOLS)["excess"]).rename("uplift")
    AV = A.set_index(KEYCOLS)[["fire_volpct", "rate"]].join(upl_arm, how="inner").reset_index()
    log(f"    {'family':<13} {'panel':<6} {'arms':>5} {'fire_volpct':>12} {'med uplift':>11}")
    fam_rows = []
    for fam in sorted(AV["family"].unique()):
        for pan in PANELS:
            s = AV[(AV["family"] == fam) & (AV["panel"] == pan)]
            if s.empty:
                continue
            fam_rows.append(dict(family=fam, panel=pan, fvp=s["fire_volpct"].median(),
                                 upl=s["uplift"].median()))
    FR = pd.DataFrame(fam_rows).sort_values("fvp")
    for r in FR.itertuples():
        log(f"    {r.family:<13} {r.panel:<6} "
            f"{len(AV[(AV['family'] == r.family) & (AV['panel'] == r.panel)]):>5} "
            f"{r.fvp:>12.3f} {r.upl:>+11.4f}")
    log(f"    rho(fire_volpct, uplift) = {spearman(FR['fvp'], FR['upl']):+.3f} over "
        f"{len(FR)} family x panel cells, "
        f"{spearman(AV['fire_volpct'], AV['uplift']):+.3f} over all {len(AV)} arms")
    below = AV[AV["fire_volpct"] < 0.5]
    above = AV[AV["fire_volpct"] >= 0.5]
    log(f"    arms firing BELOW percentile 0.500: n={len(below)}, median uplift "
        f"{below['uplift'].median():+.4f}, share>0 {(below['uplift'] > 0).mean():.3f}")
    log(f"    arms firing AT/ABOVE percentile 0.500: n={len(above)}, median uplift "
        f"{above['uplift'].median():+.4f}, share>0 {(above['uplift'] > 0).mean():.3f}")
    log("    the two falsifiers, named: BREADTH-LO is a LO gate that fires in the HIGH-vol tail")
    log("    (low breadth = a falling market), and BREADTH-HI is a HI gate that fires just below")
    log("    the median.  Both take the sign fire_volpct predicts and not the sign the LO/HI")
    log("    label predicts, which is what sinks H_MASK and H_SIGN.")

    # ======================================================== [3] Q4 - the census of the record
    log("\n[3] Q4 (COUNT) - THE RECORD'S COMMITTED LOW-TAIL PLACEBO NUMBERS, RE-PRICED")
    H, used, skipped = harvest()
    log(f"    harvested {len(H):,} committed LO-tail placebo-differenced numbers from "
        f"{len(used)} files; {len(skipped)} file(s) carried the arm key but named no null and "
        f"were SKIPPED")
    for f, n in sorted(used, key=lambda x: -x[1]):
        log(f"      {n:>7,}  {f}")
    if skipped:
        log(f"      skipped (no named null): {', '.join(skipped)}")
    log(f"    kinds present: {', '.join(sorted(H['kind'].unique()))}")

    mine3 = {k: C[C["kind"] == f"VOLBLOCK{k}"].set_index(KEYCOLS)["excess"] for k in STRATA}
    mine_b = C[C["kind"] == "BLOCK"].set_index(KEYCOLS)["excess"]
    H["panel"] = H["panel"].map(norm_panel)
    Hk = H.set_index(KEYCOLS)
    census = []
    log(f"\n    {'claim set':<8} {'k':>3} {'rows':>8} {'matched':>8} {'understated':>12} "
        f"{'med uplift':>11} {'restate>20%':>12} {'sign flips':>11} {'U56+B136 und.':>14}")
    for cs in CLAIMSETS:
        if cs == "NARROW":
            sel = Hk[Hk["kind"] == "BLOCK"]
        elif cs == "SHIFT":
            sel = Hk[Hk["kind"].isin(SHIFT_KINDS)]
        else:
            sel = Hk
        for k in STRATA:
            j = sel.join(mine3[k].rename("vb"), how="inner").join(mine_b.rename("mb"), how="inner")
            j = j.dropna(subset=["pub", "vb"])
            if j.empty:
                log(f"    {cs:<8} {k:>3} {len(sel):>8} {0:>8}  (no key overlap)")
                continue
            und = (j["vb"] > j["pub"])
            d = j["vb"] - j["pub"]
            rest = (d.abs() > MATERIAL * j["pub"].abs())
            flip = (np.sign(j["vb"]) != np.sign(j["pub"]))
            sub = j[j.index.get_level_values("panel").isin(["U56", "B136"])]
            census.append(dict(claimset=cs, k=k, rows=len(sel), matched=len(j),
                               understated=float(und.mean()), med_uplift=float(d.median()),
                               restate20=float(rest.mean()), signflip=float(flip.mean()),
                               und_u56b136=float((sub["vb"] > sub["pub"]).mean()) if len(sub) else np.nan,
                               repro_gap=float((j["mb"] - j["pub"]).abs().median())))
            log(f"    {cs:<8} {k:>3} {len(sel):>8,} {len(j):>8,} {und.mean():>12.3f} "
                f"{d.median():>+11.4f} {rest.mean():>12.3f} {flip.mean():>11.3f} "
                f"{(sub['vb'] > sub['pub']).mean() if len(sub) else float('nan'):>14.3f}")
    CEN = pd.DataFrame(census)
    narrow3 = CEN[(CEN["claimset"] == "NARROW") & (CEN["k"] == 3)]
    H_COUNT = bool(len(narrow3) and narrow3["understated"].iloc[0] >= 0.90)
    log(f"    H_COUNT (>= 90% of NARROW committed LO rows understated at k=3): "
        f"{narrow3['understated'].iloc[0]:.3f} of {int(narrow3['matched'].iloc[0]):,} matched "
        f"-> {'PASS' if H_COUNT else 'FAIL'}")
    log(f"    REPRODUCTION CONTROL - median |my BLOCK - published BLOCK| on the same keys: "
        f"{narrow3['repro_gap'].iloc[0]:.4f}  (the uplift must be read against this floor)")
    # what the record already disagrees with ITSELF by, on the same arm key
    nb = Hk[Hk["kind"] == "BLOCK"].reset_index()
    grp = nb.groupby(KEYCOLS)
    spread = grp["pub"].agg(lambda s: s.max() - s.min())
    nfiles = grp["file"].nunique()
    multi = spread[nfiles >= 2]
    log(f"    RECORD-INTERNAL FLOOR - the record's OWN committed BLOCK numbers disagree on the")
    log(f"    same arm key by a median of {multi.median():.4f} across "
        f"{int((nfiles >= 2).sum()):,} keys carried by 2+ files "
        f"(max {multi.max():.4f}); idea 871's per-arm seed noise floor is 0.0145.")
    log(f"    So the k=3 median uplift of {narrow3['med_uplift'].iloc[0]:+.4f} is "
        f"{narrow3['med_uplift'].iloc[0] / multi.median():.2f}x the record's own key-level")
    log(f"    disagreement, and the per-row understatement SHARES below are resolved only to")
    log(f"    that floor.  The per-FAMILY medians are the part that survives it.")
    log("    per-family census at the NARROW claim set, k=3:")
    selN = Hk[Hk["kind"] == "BLOCK"]
    j = selN.join(mine3[3].rename("vb"), how="inner").join(mine_b.rename("mb"), how="inner").dropna(subset=["pub", "vb"])
    log(f"      {'family':<13} {'matched':>8} {'pub med':>9} {'VOLBLOCK3':>10} {'uplift':>9} "
        f"{'understated':>12} {'restate>20%':>12}")
    for fam in sorted(j.index.get_level_values("family").unique()):
        s = j[j.index.get_level_values("family") == fam]
        d = s["vb"] - s["pub"]
        log(f"      {fam:<13} {len(s):>8,} {s['pub'].median():>+9.4f} {s['vb'].median():>+10.4f} "
            f"{d.median():>+9.4f} {(s['vb'] > s['pub']).mean():>12.3f} "
            f"{(d.abs() > MATERIAL * s['pub'].abs()).mean():>12.3f}")

    # ============================================================= [4] Q5 - rule 8 and capital
    log("\n[4] Q5 (CAPITAL) + PROTOCOL rule 8")
    log("    (a) comparands @10 bps, weekly, t+1, per panel:")
    for nm in PANELS:
        b = benches[nm]
        log(f"      {nm:<6} SPY {b['spy']['c']:.2%}/{b['spy']['s']:.3f}/{b['spy']['dd']:.2%} "
            f"(H {b['spy']['h1']:.3f}/{b['spy']['h2']:.3f}; OOS {b['spy_oos']['c']:.2%}/"
            f"{b['spy_oos']['s']:.3f}/{b['spy_oos']['dd']:.2%})   "
            f"RULES v2 {b['bl']['c']:.2%}/{b['bl']['s']:.3f}/{b['bl']['dd']:.2%} "
            f"(H {b['bl']['h1']:.3f}/{b['bl']['h2']:.3f}; OOS {b['bl_oos']['c']:.2%}/"
            f"{b['bl_oos']['s']:.3f}/{b['bl_oos']['dd']:.2%})")

    log("\n    (b) full-sample KEEP census over ALL grid points (nothing selected):")
    log(f"    {'family':<13} {'arms':>6} {'4a':>5} {'4b':>5} {'med Sharpe':>11} {'med CAGR':>10} "
        f"{'med MaxDD':>10} {'best OOS Sh':>12} {'OOS 4a':>7} {'OOS 4b':>7}")
    for fam in sorted(A["family"].unique()):
        s = A[A["family"] == fam]
        log(f"    {fam:<13} {len(s):>6} {int(s['keep4a'].sum()):>5} {int(s['keep4b'].sum()):>5} "
            f"{s['Sharpe'].median():>11.3f} {s['CAGR'].median():>10.2%} "
            f"{s['MaxDD'].median():>10.2%} {s['OOS_Sharpe'].max():>12.3f} "
            f"{int(s['oos4a'].sum()):>7} {int(s['oos4b'].sum()):>7}")
    log(f"    TOTAL         {len(A):>6} {int(A['keep4a'].sum()):>5} {int(A['keep4b'].sum()):>5}"
        f"{'':>34} {int(A['oos4a'].sum()):>19} {int(A['oos4b'].sum()):>7}")
    for side in ["LO", "HI"]:
        s = A[A["side"] == side]
        log(f"      {side}: {len(s)} arms, 4a {int(s['keep4a'].sum())}, 4b "
            f"{int(s['keep4b'].sum())}, OOS 4a {int(s['oos4a'].sum())}, OOS 4b "
            f"{int(s['oos4b'].sum())}")

    log("\n    (c) cost ladder over ALL arms, every rung reported:")
    for c in RUNGS:
        lo = A[A["side"] == "LO"]
        log(f"      {c:>2} bps  median Sharpe {A[f'Sharpe_{c}bps'].median():.3f}   "
            f"median CAGR {A[f'CAGR_{c}bps'].median():.2%}   "
            f"median MaxDD {A[f'MaxDD_{c}bps'].median():.2%}   "
            f"LO-side median Sharpe {lo[f'Sharpe_{c}bps'].median():.3f}")
    log("    and the excess itself at every rung (median over cells, k=3 vs BLOCK):")
    for c in RUNGS:
        b = C[C["kind"] == "BLOCK"]
        v = C[C["kind"] == "VOLBLOCK3"]
        for side in ["LO", "HI"]:
            log(f"      {c:>2} bps  {side}  BLOCK {b[b['side'] == side][f'excess_{c}bps'].median():+.4f}"
                f"   VOLBLOCK3 {v[v['side'] == side][f'excess_{c}bps'].median():+.4f}"
                f"   uplift {v[v['side'] == side][f'excess_{c}bps'].median() - b[b['side'] == side][f'excess_{c}bps'].median():+.4f}")

    log("\n    (d) RULE 8 - IS-ONLY SELECTOR (highest 2009-2016 Sharpe per panel x family), "
        "OOS 2017+ READ ONCE:")
    log(f"    {'panel':<6} {'family':<13} {'q':>5} {'w':>5} {'dep':>5} {'cad':>4} {'g':>5} "
        f"{'OOS CAGR':>9} {'OOS Sh':>7} {'OOS DD':>8} {'OOS H1/H2':>14} {'4a':>6} {'4b':>6}")
    picks = []
    for nm in PANELS:
        for fam in sorted(A["family"].unique()):
            s = A[(A["panel"] == nm) & (A["family"] == fam)]
            if s.empty:
                continue
            p = s.loc[s["IS_Sharpe"].idxmax()]
            picks.append(p)
            log(f"    {nm:<6} {fam:<13} {p['q']:>5.2f} {int(p['w']):>5} {p['depth']:>5.2f} "
                f"{p['cadence']:>4} {p['gross']:>5.2f} {p['OOS_CAGR']:>9.2%} "
                f"{p['OOS_Sharpe']:>7.3f} {p['OOS_MaxDD']:>8.2%} "
                f"{p['OOS_H1']:>6.3f}/{p['OOS_H2']:<7.3f} {str(bool(p['oos4a'])):>6} "
                f"{str(bool(p['oos4b'])):>6}")
    P = pd.DataFrame(picks)
    lo_p = P[P["side"] == "LO"]
    H_CAP = bool(lo_p["oos4b"].sum() > 0)
    log(f"    rule-8 picks: {len(P)}   OOS 4a {int(P['oos4a'].sum())}   OOS 4b "
        f"{int(P['oos4b'].sum())}   LO-side OOS 4b {int(lo_p['oos4b'].sum())} of {len(lo_p)}")
    log(f"    H_CAP (>= 1 LO arm's rule-8 pick clears OOS 4b): "
        f"{int(lo_p['oos4b'].sum())} -> {'PASS' if H_CAP else 'FAIL'}")

    log("\n    (e) does the RE-PRICED excess walk forward?  rho(IS excess, OOS excess), n=cells")
    log(f"    {'family':<13} " + "".join(f"{k:>13}" for k in KINDS))
    for fam in sorted(C["family"].unique()):
        row = [spearman(C[(C["family"] == fam) & (C["kind"] == k)]["excess_IS"],
                        C[(C["family"] == fam) & (C["kind"] == k)]["excess_OOS"]) for k in KINDS]
        log(f"    {fam:<13} " + "".join(f"{v:>+13.3f}" for v in row))

    # ------------------------------------------------------------------------------- verdict
    log("\n[5] PRE-REGISTERED BARS, ALL FIVE")
    for nm_, v in [("H_MASK", H_MASK), ("H_SIGN", H_SIGN), ("H_STRAT", H_STRAT),
                   ("H_COUNT", H_COUNT), ("H_CAP", H_CAP)]:
        log(f"    {nm_:<8} {'PASS' if v else 'FAIL'}")

    A.to_csv(OUT / f"{STEM}.arms.csv.gz", index=False, compression="gzip")
    C.to_csv(OUT / f"{STEM}.cells.csv.gz", index=False, compression="gzip")
    CEN.to_csv(OUT / f"{STEM}.census.csv", index=False)
    P.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    j.reset_index().to_csv(OUT / f"{STEM}.repriced.csv.gz", index=False, compression="gzip")
    log(f"\nwrote {STEM}.arms.csv.gz ({len(A)}), .cells.csv.gz ({len(C)}), "
        f".census.csv ({len(CEN)}), .picks.csv ({len(P)}), .repriced.csv.gz ({len(j)})")
    log(f"total {time.time() - t_start:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

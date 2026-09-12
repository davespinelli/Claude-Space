#!/usr/bin/env python3
"""Idea 606 - "does-the-PLACEBO-EXCESS-rate-slope-survive-outside-the-BREADTH-family" (lane B).

The finding this run exists to price
-----------------------------------
Idea 602 ran 12,960 rate-matched, information-free placebos against the record's matched-gross
twin test and killed the queue's monotone-win-rate hypothesis outright.  ONE positive result
survived: the PLACEBO-DIFFERENCED statistic inside the rolling breadth quantile family.  The
median excess of a real QROLL arm's dSharpe over its OWN rate/depth/gross/panel-matched BLOCK
placebo rose +0.026 -> +0.045 -> +0.070 -> +0.069 -> +0.102 across five equal-count rate
buckets, with the share of arms beating their own placebo rising 0.925 -> 1.000.  Read as a
claim about gates, that says: a gate that fires more often buys more information per unit of
firing.  Read as a claim about BREADTH, it says only that this one signal does.

The two readings are not separable inside the breadth family, because every arm in idea 602's
grid is a function of the SAME state - the share of panel names above their 200d MA.  This run
separates them the only way available: build the identical machinery (identical book, identical
matched-gross twin, identical BLOCK/RAND placebos, identical buckets) on gate states that have
NOTHING to do with breadth, and read the same curve.

The questions, stated so they can be answered either way
--------------------------------------------------------
    Q1 (CONTROL)     Does the breadth curve reproduce?  G3 re-derives idea 602's committed
                     curve from its own excess.csv; [4] rebuilds it from scratch here.
    Q2 (SLOPE)       Is the excess-vs-BLOCK curve rising in the realised firing rate on the
                     NON-BREADTH states?  Pre-registered bar, borrowed verbatim from idea
                     602's own Q1: every adjacent equal-count bucket step non-decreasing AND
                     Spearman(bucket, median excess) >= +0.80, at EVERY bucket count K and
                     under BOTH bucket units.  Reported for all 8 families at all 10 readings.
    Q3 (LEVEL)       Is the excess non-zero AT ALL outside breadth?  A slope on a zero level is
                     not a finding.  Median excess and share>0 per family, with a sign test.
    Q4 (DIRECTION)   Is any of it about the gate FIRING or about the SIGN of the state?  Every
                     state is run in both directions (fire on the low tail AND on the high
                     tail); the reversed arm fires at the same rate with the same clustering
                     and the opposite information, so it is a second, sharper placebo.
    Q5 (CONTROL)     Any 4b pass this grid throws up is priced against the ONE comparand 4b
                     structurally cannot see: the arm's own gross-matched twin, and the
                     ungated book itself.  Idea 596's bar - clear 4b on both windows AND beat
                     a twin that 4b rejects - is applied verbatim.
    Q6 (RULE 8)      Both PROTOCOL KEEP paths on every grid point, the rule-8 chooser over
                     (level, w) per panel x family x depth x cadence x gross x rung with OOS
                     CAGR/Sharpe/MaxDD read once against RULES v2 and SPY, and the CLAIM's own
                     out-of-sample test: the excess re-measured on the IS window alone and read
                     again on 2017+, per arm and per bucket.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. state        the gate's state variable: VOL20 / DISP / CORR, with BREADTH inherited
                    verbatim from idea 602 as the control.  Direction is NOT a third parameter:
                    both directions of every state are always reported, never selected on.
    2. rate bucket  K equal-count buckets of the realised firing rate, K in {3,4,5,6,8}, plus
                    an equal-WIDTH reading at each K as a second unit (idea 590's point).
    ALL grid points reported at every panel / family / level / w / depth / cadence / gross /
    cost rung.  Nothing is chosen on the answer.

Reported axes, NEVER tuned or selected on (all inherited from idea 602 verbatim)
    level q  0.07 / 0.12 / 0.17      w  252 / 504 / 1008 / 2016    depth  0.25 / 0.50 / 1.00
    cadence  D / W                   gross  0.75 / 1.00            cost   0 / 10 / 25 bps
    panel    U56 / B136 / SMALL664

The four states, all computed from the panel's own closes and nothing else
    BREADTH  share of priced names above their own 200d MA                (idea 602 verbatim)
    VOL20    cross-sectional MEAN of 20d annualised realised vol
    DISP     20d mean of the daily cross-sectional STD of returns
    CORR     20d average pairwise correlation, the equal-weight index-vs-name variance identity
             rho = (s_idx^2 - s2bar/N) / (sbar^2 - s2bar/N)
  The three new states share ONE smoothing window (20 days), fixed in advance, never swept.
  PRIOR DIRECTION, declared before the run: breadth fires on its LOW tail (602's), vol /
  dispersion / correlation fire on their HIGH tail.  The other four families are the
  sign-reversed controls and are labelled as such throughout.

Reproduction gates (section [0], printed before any new number is read)
    G1  derived cost rung r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=c).
    G2  idea 84's ungated EWALL U56 g=0.85 @10bps: 11.8% / 1.05 / -17.9% / H 1.07 / 1.04.
    G3  idea 602's COMMITTED .excess.csv: its QROLL K=5 curve re-derived here must give
        +0.0259 / +0.0446 / +0.0705 / +0.0695 / +0.1017 and share>0 0.925 / 0.966 / 0.992 /
        1.000 / 1.000.  This is the number this run is testing the generality of.
    G4  twin interpolation: the 0.01 gross cache interpolated to an exact g vs a true
        engine.backtest at that exact g, 6 off-grid values per panel.
    G5  placebo matching identity: RAND and BLOCK reproduce the real arm's de-grossed day count
        and mean multiplier exactly, so they share its twin exactly.
    G6  the fast Sharpe used on the 69k placebo cells equals engine.metrics()["Sharpe"].

Data: committed caches only, no network, never yfinance.  SURVIVORSHIP: all three panels are
current-constituent lists, so CAGR and drawdown LEVELS are optimistic; the gate-vs-twin CONTRAST
and the placebo differencing are the durable part.  SMALL664 starts 2010-01-04 and is NOT idea
602's SMALL439 panel (that cache has since been rebuilt), so G3 is priced on the two panels
whose membership is unchanged and the small panel is reported as a fresh measurement.

Deterministic (all placebo seeds are md5-derived), standalone.  Reads baseline.py and engine;
modifies nothing.
"""
import hashlib
import os
import sys
import time
from itertools import product
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
PARENT_EXCESS = OUT / "2026-09-10_is-the-MATCHED-GROSS-TWIN-win-rate-a-FIRING-RATE-function_C.excess.csv"

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 1.00]
QS = [0.07, 0.12, 0.17]
WS = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
KS = [3, 4, 5, 6, 8]
UNITS = ["count", "width"]
RUNGS = [0, 10, 25]
RUNG_HEAD = 10
CADENCES = ["D", "W"]
SMOOTH = 20
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TIE = 1e-12
NSEED = 10
GSTEP = 0.01
SLOPE_BAR = 0.80

STATES = ["BREADTH", "VOL20", "DISP", "CORR"]
PRIOR_SIDE = {"BREADTH": "LO", "VOL20": "HI", "DISP": "HI", "CORR": "HI"}
FAMILIES = [f"{s}-{side}" for s in STATES for side in ("LO", "HI")]
PRIOR_FAMS = [f"{s}-{PRIOR_SIDE[s]}" for s in STATES]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

LINES = []
T0 = time.time()

# Staging only (the sandbox suspends a process between turns, so the three panels are computed
# one per invocation).  With neither variable set the script computes everything in one process;
# nothing in a panel's computation reads another panel, so the two paths are bit-identical.
CACHE = Path(os.environ["IDEA606_CACHE"]) if os.environ.get("IDEA606_CACHE") else None
ONLY = [s for s in os.environ.get("IDEA606_ONLY", "").split(",") if s]


def log(s=""):
    print(s)
    LINES.append(str(s))


# ---------------------------------------------------------------- primitives (idea 42/399/602)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def sharpe(r):
    """engine.metrics()['Sharpe'] on a numpy array; G6 prices the identity."""
    v = np.asarray(r, float)
    sd = v.std(ddof=1)
    return v.mean() * 252 / (sd * np.sqrt(252)) if sd > 0 else np.nan


def state_breadth(px):
    """idea 602 verbatim."""
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def state_vol20(px):
    v = px.pct_change().rolling(SMOOTH).std() * np.sqrt(252)
    return v.mean(axis=1)


def state_disp(px):
    return px.pct_change().std(axis=1).rolling(SMOOTH).mean()


def state_corr(px):
    """20d average pairwise correlation from the equal-weight index-vs-name variance identity."""
    rt = px.pct_change()
    sig = rt.rolling(SMOOTH).std()
    idx = rt.mean(axis=1)
    s_idx = idx.rolling(SMOOTH).std()
    n = sig.notna().sum(axis=1).replace(0, np.nan)
    sbar = sig.mean(axis=1)
    s2bar = (sig ** 2).mean(axis=1)
    num = s_idx ** 2 - s2bar / n
    den = sbar ** 2 - s2bar / n
    return (num / den.replace(0, np.nan)).clip(-1, 1)


STATE_FN = {"BREADTH": state_breadth, "VOL20": state_vol20, "DISP": state_disp, "CORR": state_corr}


def _cadence(m, idx):
    mask = rebalance_mask(idx, FREQ)
    return m.where(mask).ffill().fillna(1.0)


def gate_mult(st, thr, side, depth, cadence, idx):
    """Fire (de-gross to 1-depth) when the state is in its bad tail; 1.0 before the threshold
    exists.  side LO fires on st < thr (breadth's direction), HI fires on st > thr."""
    fire = (st < thr) if side == "LO" else (st > thr)
    fire = fire & st.notna() & thr.notna()
    m = pd.Series(1.0, index=idx).where(~fire, 1.0 - depth)
    return _cadence(m, idx) if cadence == "W" else m


def apply_eff(r_base, m_eff, gross, cost_bps):
    """Apply an ALREADY-EFFECTIVE (t+1-aligned) multiplier path, with idea 399's switch cost."""
    switch = m_eff.diff().abs().fillna(0.0)
    return m_eff * r_base - switch * gross * cost_bps / 1e4


def apply_gate(r_base, mult, gross, cost_bps):
    """idea 399 verbatim: multiplier decided at t, applied at t+1, switch cost on |dm|."""
    m_eff = mult.reindex(r_base.index).shift(1).fillna(1.0)
    return apply_eff(r_base, m_eff, gross, cost_bps), m_eff


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def pack_of(r):
    """(H1, H2, OOS Sharpe, MaxDD, CAGR) of a benchmark over a window."""
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    return (h1, h2, metrics(r.loc[OOS_START:])["Sharpe"], m["MaxDD"], m["CAGR"])


def tests_4b(r, pk):
    s1, s2, s_oos, s_dd, s_cagr = pk
    h1, h2 = half_sharpes(r)
    m = metrics(r)
    return {"H1": h1 > s1, "H2": h2 > s2,
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] > s_oos,
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(s_dd),
            "CAGR": m["CAGR"] >= 0.70 * s_cagr}


def tests_4b_window(r, pk):
    """4b read INSIDE one window (used for the OOS-only verdict): halves of that window."""
    s1, s2, s_dd, s_cagr = pk
    h1, h2 = half_sharpes(r)
    m = metrics(r)
    return {"H1": h1 > s1, "H2": h2 > s2, "DD": abs(m["MaxDD"]) <= 0.60 * abs(s_dd),
            "CAGR": m["CAGR"] >= 0.70 * s_cagr}


def verdict_4a(r, bp):
    b1, b2, bdd = bp
    h1, h2 = half_sharpes(r)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= bdd)


def summarise(r, spy_pack, base_pack, spy_oos_pack, base_oos_pack):
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    m_is, m_oos = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    t = tests_4b(r, spy_pack)
    ro = r.loc[OOS_START:]
    to = tests_4b_window(ro, spy_oos_pack)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=m_is["Sharpe"], OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"],
                OOS_MaxDD=m_oos["MaxDD"], p4a=verdict_4a(r, base_pack), p4b=all(t.values()),
                p4a_oos=verdict_4a(ro, base_oos_pack), p4b_oos=all(to.values()),
                fail4b=",".join([k for k, v in t.items() if not v]) or "-")


def spearman(a, b):
    a, b = pd.Series(list(a)), pd.Series(list(b))
    if a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.rank().corr(b.rank()))


def bucket(v, K, unit):
    v = pd.Series(np.asarray(v, float))
    try:
        if unit == "count":
            b = pd.qcut(v.rank(method="first"), K, labels=False)
        else:
            b = pd.cut(v, K, labels=False)
    except ValueError:
        return pd.Series(np.nan, index=v.index)
    return b.astype(float)


def sign_test_p(k, n):
    """Two-sided exact binomial p at p0=0.5 (no scipy)."""
    if n == 0:
        return np.nan
    from math import comb
    tail = min(k, n - k)
    p = sum(comb(n, i) for i in range(0, tail + 1)) / 2 ** n
    return min(1.0, 2 * p)


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


# ---------------------------------------------------------------- twin machinery (idea 602)
class Twins:
    """Static-gross EWALL twin returns at an exact g by linear interpolation on a GSTEP cache."""

    def __init__(self, px, start):
        self.px, self.start = px, start
        self.cache = {}
        self.rcache = {}
        self.n_bt = 0

    def _exact(self, g):
        g = round(g, 6)
        if g not in self.cache:
            res = backtest(self.px, ewall_weights(self.px, g), cost_bps=0, freq=FREQ)
            self.cache[g] = (res["returns"].loc[self.start:], res["turnover"].loc[self.start:])
            self.n_bt += 1
        return self.cache[g]

    def prewarm(self, gs):
        need = set()
        for g in gs:
            lo = np.floor(round(g, 6) / GSTEP) * GSTEP
            need.add(round(lo, 6))
            need.add(round(lo + GSTEP, 6))
        for g in sorted(need):
            self._exact(g)

    def at(self, g, cost_bps):
        key = (round(g, 6), cost_bps)
        if key in self.rcache:
            return self.rcache[key]
        lo = round(np.floor(round(g, 6) / GSTEP) * GSTEP, 6)
        lam = (round(g, 6) - lo) / GSTEP
        if lam <= 1e-9:
            r0, t0 = self._exact(lo)
        else:
            rl, tl = self._exact(lo)
            rh, th = self._exact(round(lo + GSTEP, 6))
            r0, t0 = (1 - lam) * rl + lam * rh, (1 - lam) * tl + lam * th
        out = r0 - t0 * cost_bps / 1e4
        if len(self.rcache) < 4000:
            self.rcache[key] = out
        return out


# ---------------------------------------------------------------- placebos (idea 602 verbatim)
def seed_of(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def placebo_mults(m_eff, depth, kind, seed):
    """Rate-matched, information-free twin of the EFFECTIVE multiplier path m_eff.
    RAND : iid days, EXACTLY the same number of de-grossed days.
    BLOCK: circular shift of m_eff - exact rate AND exact run-length distribution."""
    v = m_eff.values
    k = int((v < 1.0).sum())
    if k == 0:
        return m_eff.copy()
    rng = np.random.default_rng(seed)
    if kind == "RAND":
        out = np.ones(len(v))
        out[rng.choice(len(v), size=k, replace=False)] = 1.0 - depth
        return pd.Series(out, index=m_eff.index)
    shift = int(rng.integers(1, len(v)))
    return pd.Series(np.roll(v, shift), index=m_eff.index)


# =============================================================================== per-panel run
def run_panel(panel, px):
    """Compute every per-panel row.  Returns (meta, cells, placebos, gates, g4, g5).

    The caller may persist the return value (env IDEA606_CACHE) so a long run can be executed
    one panel per invocation; with no cache set the script computes all three in one process
    and is bit-identical either way (nothing here reads another panel's state)."""
    gates_log, cells, ph, g4, g5 = [], [], [], [], []
    line0 = len(LINES)
    start = px.index[260]
    idx = px.index
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_pack = pack_of(spy)
    spy_o = spy.loc[OOS_START:]
    m_so = metrics(spy_o)
    h1o, h2o = half_sharpes(spy_o)
    spy_oos_pack = (h1o, h2o, m_so["MaxDD"], m_so["CAGR"])

    log(f"\n{'='*185}\nPANEL {panel}: {px.shape[1]} columns, {idx[0].date()} -> {idx[-1].date()}, "
        f"eval from {start.date()} ({len(spy)} days)")
    m_spy = metrics(spy)
    log(f"  SPY {m_spy['CAGR']:.2%} / {m_spy['Sharpe']:.3f} / {m_spy['MaxDD']:.2%}; "
        f"4b bars: CAGR floor {0.70*m_spy['CAGR']:.2%}, "
        f"DD cap {-0.60*abs(m_spy['MaxDD']):.2%}, halves {spy_pack[0]:.3f}/{spy_pack[1]:.3f}, "
        f"OOS {spy_pack[2]:.3f}")

    # ---- states and thresholds
    sts = {s: STATE_FN[s](px) for s in STATES}
    # LO families cut at q; HI families cut at 1-q (same tail mass on the other side)
    thr_lo = {(s, q, w): sts[s].rolling(w, min_periods=w).quantile(q)
              for s in STATES for q in QS for w in WS}
    thr_hi = {(s, q, w): sts[s].rolling(w, min_periods=w).quantile(1 - q)
              for s in STATES for q in QS for w in WS}

    # ---- base books at 0 bps, all rungs derived (G1)
    base0 = {}
    for g in GROSSES:
        res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
        base0[g] = (res["returns"].loc[start:], res["turnover"].loc[start:])

    def rung(pack, c):
        r0, t0 = pack
        return r0 - t0 * c / 1e4

    # ---- G1
    live = backtest(px, ewall_weights(px, 0.75), cost_bps=RUNG_HEAD, freq=FREQ)["returns"].loc[start:]
    g1 = float((rung(base0[0.75], RUNG_HEAD) - live).abs().max())

    # ---- baselines
    base_packs, base_oos_packs, base_rows = {}, {}, {}
    for c in RUNGS:
        b = backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
        b1, b2 = half_sharpes(b)
        base_packs[c] = (b1, b2, metrics(b)["MaxDD"])
        bo = b.loc[OOS_START:]
        bo1, bo2 = half_sharpes(bo)
        base_oos_packs[c] = (bo1, bo2, metrics(bo)["MaxDD"])
        base_rows[c] = dict(CAGR=metrics(b)["CAGR"], Sharpe=metrics(b)["Sharpe"],
                            MaxDD=metrics(b)["MaxDD"], H1=b1, H2=b2,
                            OOS_CAGR=metrics(bo)["CAGR"], OOS_Sharpe=metrics(bo)["Sharpe"],
                            OOS_MaxDD=metrics(bo)["MaxDD"])
    v1 = backtest(px, rules_v1_weights(px), cost_bps=RUNG_HEAD, freq=FREQ)["returns"].loc[start:]
    log(f"  RULES v2 @10bps {base_rows[10]['CAGR']:.2%} / {base_rows[10]['Sharpe']:.3f} / "
        f"{base_rows[10]['MaxDD']:.2%} (H {base_rows[10]['H1']:.3f}/{base_rows[10]['H2']:.3f}); "
        f"RULES v1 @10bps {metrics(v1)['CAGR']:.2%} / {metrics(v1)['Sharpe']:.3f} / "
        f"{metrics(v1)['MaxDD']:.2%}")

    # ---- arm specs and their effective multipliers (rate is gross- and rung-independent)
    arms = [(f"{s}-{side}", s, side, q, w) for s in STATES for side in ("LO", "HI")
            for q in QS for w in WS]
    r_ref = base0[0.75][0]
    mult, on_cache, gap_cache = {}, {}, {}
    for fam, s, side, q, w in arms:
        th = (thr_lo if side == "LO" else thr_hi)[(s, q, w)]
        for d, cad in product(DEPTHS, CADENCES):
            m = gate_mult(sts[s], th, side, d, cad, idx)
            me = m.reindex(r_ref.index).shift(1).fillna(1.0)
            key = (fam, q, w, d, cad)
            mult[key] = m
            on_cache[key] = float((me < 1.0).mean())
            gap_cache[key] = 1.0 - float(me.mean())

    for fam, s, side, q, w in arms:
        gates_log.append(dict(panel=panel, family=fam, state=s, side=side, level=q, w=w,
                              prior=fam in PRIOR_FAMS,
                              on_D=on_cache.get((fam, q, w, DEPTHS[0], "D"), np.nan),
                              on_W=on_cache.get((fam, q, w, DEPTHS[0], "W"), np.nan),
                              armed=float((sts[s].loc[start:].notna()
                                           & (thr_lo if side == "LO" else thr_hi)[(s, q, w)]
                                           .loc[start:].notna()).mean())))

    # ---- twin prewarm
    need = []
    for g in GROSSES:
        for key in mult:
            need.append(g * (1.0 - gap_cache[key]))
    tw = Twins(px, start)
    tw.prewarm(need)

    # ---- G4 interpolation error
    rng4 = np.random.default_rng(seed_of(panel, "G4"))
    for gtest in np.round(np.sort(rng4.uniform(min(need), max(need), 6)), 4):
        true = backtest(px, ewall_weights(px, float(gtest)), cost_bps=0,
                        freq=FREQ)["returns"].loc[start:]
        g4.append(dict(panel=panel, g=float(gtest),
                       max_abs=float((tw.at(float(gtest), 0) - true).abs().max()),
                       dSharpe=float(sharpe(tw.at(float(gtest), 0)) - sharpe(true))))

    # ---- main grid
    for c in RUNGS:
        for g in GROSSES:
            rb = rung(base0[g], c)
            for fam, s, side, q, w in arms:
                for d, cad in product(DEPTHS, CADENCES):
                    key = (fam, q, w, d, cad)
                    rg, me = apply_gate(rb, mult[key], g, c)
                    g_eff = g * (1.0 - gap_cache[key])
                    rs = tw.at(g_eff, c)
                    mg, mst = metrics(rg), metrics(rs)
                    dsh = mg["Sharpe"] - mst["Sharpe"]
                    row = dict(panel=panel, rung=c, gross=g, family=fam, state=s, side=side,
                               prior=fam in PRIOR_FAMS, level=q, w=w, depth=d, cadence=cad,
                               on_share=on_cache[key], gap=gap_cache[key], g_eff=g_eff,
                               twin_Sharpe=mst["Sharpe"], dSharpe=dsh,
                               dOOS=sharpe(rg.loc[OOS_START:]) - sharpe(rs.loc[OOS_START:]),
                               dIS=sharpe(rg.loc[:IS_END]) - sharpe(rs.loc[:IS_END]),
                               dCAGR=mg["CAGR"] - mst["CAGR"],
                               dMaxDD=abs(mst["MaxDD"]) - abs(mg["MaxDD"]),
                               win=bool(dsh > TIE), tie=bool(abs(dsh) <= TIE),
                               **summarise(rg, spy_pack, base_packs[c], spy_oos_pack,
                                           base_oos_packs[c]))
                    cells.append(row)

                    if c != RUNG_HEAD:
                        continue
                    # ---- placebos at the head rung only; same g_eff => same twin (G5)
                    s_full_t, s_is_t, s_oos_t = (sharpe(rs), sharpe(rs.loc[:IS_END]),
                                                 sharpe(rs.loc[OOS_START:]))
                    for kind in ("RAND", "BLOCK"):
                        for sd in range(NSEED):
                            pm = placebo_mults(me, d, kind, seed_of(panel, fam, q, w, d, cad, g,
                                                                   kind, sd))
                            rp = apply_eff(rb, pm, g, c)
                            gp = g * float(pm.mean())
                            if abs(gp - g_eff) > 1e-9:
                                rsp = tw.at(gp, c)
                                s_f, s_i, s_o = (sharpe(rsp), sharpe(rsp.loc[:IS_END]),
                                                 sharpe(rsp.loc[OOS_START:]))
                            else:
                                s_f, s_i, s_o = s_full_t, s_is_t, s_oos_t
                            ph.append(dict(panel=panel, kind=kind, seed=sd, family=fam, state=s,
                                           side=side, prior=fam in PRIOR_FAMS, level=q, w=w,
                                           depth=d, cadence=cad,
                                           gross=g, on_share=float((pm < 1.0).mean()),
                                           gap=1.0 - float(pm.mean()),
                                           real_on=on_cache[key], real_gap=gap_cache[key],
                                           dSharpe=sharpe(rp) - s_f,
                                           dIS=sharpe(rp.loc[:IS_END]) - s_i,
                                           dOOS=sharpe(rp.loc[OOS_START:]) - s_o))
                            if sd == 0:
                                g5.append(dict(panel=panel, family=fam, level=q, w=w, depth=d,
                                               cadence=cad, gross=g, kind=kind,
                                               d_on=abs(float((pm < 1.0).mean()) - on_cache[key]),
                                               d_gap=abs((1.0 - float(pm.mean())) - gap_cache[key])))
        log(f"    rung {c:>2} bps done ({time.time()-T0:.0f}s, twin backtests {tw.n_bt}, "
            f"cells {len(cells)}, placebos {len(ph)})")

    meta = dict(panel=panel, spy_pack=spy_pack, spy_oos_pack=spy_oos_pack,
                base_rows=base_rows, g1=g1, start=str(start.date()),
                spy_row=dict(CAGR=m_spy["CAGR"], Sharpe=m_spy["Sharpe"],
                             MaxDD=m_spy["MaxDD"], H1=spy_pack[0], H2=spy_pack[1],
                             OOS_CAGR=metrics(spy_o)["CAGR"], OOS_Sharpe=metrics(spy_o)["Sharpe"],
                             OOS_MaxDD=metrics(spy_o)["MaxDD"]),
                head_lines=list(LINES[line0:]))
    return meta, cells, ph, gates_log, g4, g5


# =============================================================================== main
def main():
    log(__doc__)
    log("=" * 185)
    log("[0] REPRODUCTION GATES")

    # ---- G3 first: idea 602's committed curve, re-derived from its own rows
    pe = pd.read_csv(PARENT_EXCESS)
    qr = pe[pe["family"] == "QROLL"]
    g3_med = qr.pivot_table(index="family", columns="bk", values="excess_vs_BLOCK",
                            aggfunc="median").iloc[0]
    g3_pos = qr.assign(pos=qr["excess_vs_BLOCK"] > 0).pivot_table(
        index="family", columns="bk", values="pos", aggfunc="mean").iloc[0]
    tgt_med = [0.0259, 0.0446, 0.0705, 0.0695, 0.1017]
    tgt_pos = [0.925, 0.9655, 0.9915, 1.0, 1.0]
    g3_ok = (max(abs(g3_med.values[i] - tgt_med[i]) for i in range(5)) < 5e-4
             and max(abs(g3_pos.values[i] - tgt_pos[i]) for i in range(5)) < 5e-4)
    log(f"  G3 idea 602's committed QROLL curve ({len(qr)} rows): median excess_vs_BLOCK "
        + " / ".join(f"{v:+.4f}" for v in g3_med.values))
    log(f"     share>0 " + " / ".join(f"{v:.3f}" for v in g3_pos.values)
        + f"   -> {'PASS' if g3_ok else 'FAIL'} (the claim this run generalises)")

    # ---- G6 fast Sharpe identity
    rng = np.random.default_rng(0)
    tst = pd.Series(rng.normal(0, 0.01, 3000))
    g6 = abs(sharpe(tst) - metrics(tst)["Sharpe"])
    log(f"  G6 fast Sharpe vs engine.metrics()['Sharpe']: {g6:.3e} -> "
        f"{'PASS' if g6 < 1e-12 else 'FAIL'}")

    panels = {}
    px_u = load_universe()
    panels["U56"] = px_u
    panels["B136"] = load_universe(broad=True)
    px_s, n_drop = small_panel()
    panels[f"SMALL{px_s.shape[1]-1}"] = px_s
    log(f"  small panel: {n_drop} tickers with max_1d_move >= 1.0 dropped, "
        f"{px_s.shape[1]-1} names + SPY")

    # ---- G2 idea 84
    st_u = px_u.index[260]
    r84 = backtest(px_u, ewall_weights(px_u, 0.85), cost_bps=10, freq=FREQ)["returns"].loc[st_u:]
    m84 = metrics(r84)
    h84 = half_sharpes(r84)
    g2_ok = (abs(m84["CAGR"] - 0.118) < 0.002 and abs(m84["Sharpe"] - 1.05) < 0.02
             and abs(m84["MaxDD"] + 0.179) < 0.004)
    log(f"  G2 idea 84 EWALL U56 g=0.85 @10bps: {m84['CAGR']:.2%} / {m84['Sharpe']:.3f} / "
        f"{m84['MaxDD']:.2%} / H {h84[0]:.3f}/{h84[1]:.3f}  (target 11.8%/1.05/-17.9%/1.07/1.04) "
        f"-> {'PASS' if g2_ok else 'FAIL'}")

    cells, ph, gates_log, g4, g5 = [], [], [], [], []
    meta = {}
    missing = []
    for name, px in panels.items():
        cf = (CACHE / f"{STEM}.{name}.pkl") if CACHE else None
        if cf is not None and cf.exists():
            m, c, p, gl, a4, a5 = pd.read_pickle(cf)
            LINES.extend(m["head_lines"])
            print("\n".join(m["head_lines"]))
        elif ONLY and name not in ONLY:
            missing.append(name)
            continue
        else:
            m, c, p, gl, a4, a5 = run_panel(name, px)
            if cf is not None:
                pd.to_pickle((m, c, p, gl, a4, a5), cf)
        meta[name] = m
        cells += c
        ph += p
        gates_log += gl
        g4 += a4
        g5 += a5
    if missing:
        log(f"\n  STAGED RUN: panels {missing} not computed in this invocation and not cached; "
            f"re-run with IDEA606_ONLY covering them, then again with none, to produce the "
            f"analysis.  No analysis written.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
        return

    gc = pd.DataFrame(cells)
    ph = pd.DataFrame(ph)
    gates = pd.DataFrame(gates_log)
    g4 = pd.DataFrame(g4)
    g5 = pd.DataFrame(g5)

    log(f"\n  G1 derived cost rung vs live engine.backtest(cost_bps=10), max |diff| per panel: "
        + ", ".join(f"{k} {v['g1']:.3e}" for k, v in meta.items())
        + f" -> {'PASS' if max(v['g1'] for v in meta.values()) < 1e-12 else 'FAIL'}")
    log(f"  G4 twin interpolation vs a true backtest at the exact g ({len(g4)} off-grid values): "
        f"max |return diff| {g4['max_abs'].max():.3e}, max |dSharpe| {g4['dSharpe'].abs().max():.3e} "
        f"-> {'PASS' if g4['dSharpe'].abs().max() < 0.02 else 'FAIL'}")
    log(f"  G5 placebo matching identity over {len(g5)} arm x kind checks: max |d on_share| "
        f"{g5['d_on'].max():.3e}, max |d gap| {g5['d_gap'].max():.3e} -> "
        f"{'PASS' if max(g5['d_on'].max(), g5['d_gap'].max()) < 1e-12 else 'FAIL'}")

    # =========================================================== [1] the states and their rates
    log("\n" + "=" * 185)
    log("[1] THE FOUR STATES AND THEIR REALISED FIRING RATES")
    log("  on_share = share of evaluated days the book is de-grossed (depth-independent).")
    log(gates.groupby(["panel", "family"])[["on_D", "on_W", "armed"]].mean().to_string(
        float_format=lambda x: f"{x:.4f}"))
    log("\n  by nominal level q (pooled over panels, w, cadence):")
    piv = gates.melt(id_vars=["panel", "family", "level", "w"], value_vars=["on_D", "on_W"],
                     var_name="cad", value_name="on")
    log(piv.pivot_table(index="family", columns="level", values="on",
                        aggfunc="median").to_string(float_format=lambda x: f"{x:.4f}"))
    log("\n  NOTE: a rolling quantile does NOT fire at its nominal rate (the 2026-09-10 result);")
    log("  the realised rate is what every bucket in this run is cut on.")

    # =========================================================== [2] real arms vs their twins
    log("\n" + "=" * 185)
    log("[2] Q1/Q4 - THE REAL ARMS AGAINST THEIR MATCHED-GROSS TWINS")
    head = gc[gc["rung"] == RUNG_HEAD].copy()
    log(f"  {len(gc)} gated cells, {len(head)} at the {RUNG_HEAD} bps head rung. "
        f"ties (|dSharpe| <= {TIE:g}): {int(gc['tie'].sum())}")
    log(head.groupby(["family", "prior"])["win"].agg(["size", "mean"]).to_string(
        float_format=lambda x: f"{x:.4f}"))
    log("\n  median dSharpe (real minus its own matched-gross twin), by panel x family:")
    log(head.pivot_table(index="family", columns="panel", values="dSharpe",
                         aggfunc="median").to_string(float_format=lambda x: f"{x:+.4f}"))

    # =========================================================== [3] the placebo excess
    log("\n" + "=" * 185)
    log("[3] Q3 - THE PLACEBO EXCESS, LEVEL")
    log(f"  {len(ph)} placebo cells = {NSEED} seeds x 2 kinds x {len(head)} head-rung arms.")
    key = ["panel", "family", "state", "side", "prior", "level", "w", "depth", "cadence", "gross"]
    pm = ph.groupby(key + ["kind"])[["dSharpe", "dIS", "dOOS"]].mean().unstack("kind")
    pm.columns = [f"{a}_{b}" for a, b in pm.columns]
    hh = head.set_index(key)[["dSharpe", "dIS", "dOOS", "on_share"]].rename(
        columns={"dSharpe": "REAL", "dIS": "REAL_IS", "dOOS": "REAL_OOS"})
    ex = pm.join(hh).reset_index()
    ex["excess_vs_RAND"] = ex["REAL"] - ex["dSharpe_RAND"]
    ex["excess_vs_BLOCK"] = ex["REAL"] - ex["dSharpe_BLOCK"]
    ex["excess_IS"] = ex["REAL_IS"] - ex["dIS_BLOCK"]
    ex["excess_OOS"] = ex["REAL_OOS"] - ex["dOOS_BLOCK"]
    log("  median by family (REAL = the arm's own dSharpe; BLOCK/RAND = its matched placebos):")
    tab = ex.groupby(["family", "prior"])[["REAL", "dSharpe_RAND", "dSharpe_BLOCK",
                                           "excess_vs_RAND", "excess_vs_BLOCK"]].median()
    tab.columns = ["REAL", "RAND", "BLOCK", "exc_RAND", "exc_BLOCK"]
    log(tab.to_string(float_format=lambda x: f"{x:+.4f}"))
    log("\n  share of arms whose REAL dSharpe beats its own placebo mean (+ exact sign test p):")
    sh = ex.groupby("family").apply(lambda s: pd.Series({
        "n": len(s), "vs_RAND": float((s["excess_vs_RAND"] > 0).mean()),
        "vs_BLOCK": float((s["excess_vs_BLOCK"] > 0).mean()),
        "p_BLOCK": sign_test_p(int((s["excess_vs_BLOCK"] > 0).sum()), len(s))}),
        include_groups=False)
    log(sh.to_string(float_format=lambda x: f"{x:.4f}"))

    # =========================================================== [4] THE HEADLINE: the slope
    log("\n" + "=" * 185)
    log("[4] Q2 - THE HEADLINE: IS THE EXCESS RISING IN THE REALISED FIRING RATE?")
    log(f"  Pre-registered bar (idea 602's own): every adjacent bucket step non-decreasing AND")
    log(f"  Spearman(bucket, median excess) >= +{SLOPE_BAR:.2f}, at EVERY K and BOTH units.")
    rows = []
    for K, unit in product(KS, UNITS):
        e = ex.copy()
        e["bk"] = bucket(e["on_share"], K, unit)          # pooled edges, idea 602's convention
        e = e.dropna(subset=["bk"])
        for fam, sub in e.groupby("family"):
            med = sub.groupby("bk")["excess_vs_BLOCK"].median().sort_index()
            pos = sub.groupby("bk").apply(lambda s: float((s["excess_vs_BLOCK"] > 0).mean()),
                                          include_groups=False).sort_index()
            n = sub.groupby("bk").size().sort_index()
            st = np.diff(med.values)
            rows.append(dict(K=K, unit=unit, family=fam, prior=fam in PRIOR_FAMS,
                             buckets=len(med), n=len(sub),
                             first=med.values[0], last=med.values[-1],
                             span=med.values[-1] - med.values[0],
                             monotone_up=bool(len(st) and (st >= -1e-12).all()),
                             rho=spearman(range(len(med)), med.values),
                             pos_first=pos.values[0], pos_last=pos.values[-1],
                             min_n=int(n.min())))
    sl = pd.DataFrame(rows)
    sl["passes"] = sl["monotone_up"] & (sl["rho"] >= SLOPE_BAR)
    log("\n  Per-family verdict over the 10 readings (5 K x 2 units):")
    summ = sl.groupby(["family", "prior"]).agg(
        readings=("passes", "size"), passes=("passes", "sum"),
        monotone=("monotone_up", "sum"), rho_med=("rho", "median"),
        span_med=("span", "median")).reset_index()
    log(summ.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    log("\n  Full ladder (every K x unit x family):")
    log(sl.sort_values(["family", "unit", "K"]).to_string(
        index=False, float_format=lambda x: f"{x:+.4f}"))
    log("\n  K=5 equal-count curves (idea 602's headline reading), median excess_vs_BLOCK:")
    e5 = ex.copy()
    e5["bk"] = bucket(e5["on_share"], 5, "count")
    log(e5.pivot_table(index="family", columns="bk", values="excess_vs_BLOCK",
                       aggfunc="median").to_string(float_format=lambda x: f"{x:+.4f}"))
    log("  share > 0:")
    log(e5.assign(pos=e5["excess_vs_BLOCK"] > 0).pivot_table(
        index="family", columns="bk", values="pos", aggfunc="mean").to_string(
        float_format=lambda x: f"{x:.3f}"))
    log("  bucket median realised rate:")
    log(e5.pivot_table(index="family", columns="bk", values="on_share",
                       aggfunc="median").to_string(float_format=lambda x: f"{x:.3f}"))
    log("  n:")
    log(e5.pivot_table(index="family", columns="bk", values="excess_vs_BLOCK",
                       aggfunc="size").to_string())
    log("\n  BREADTH-LO here is idea 602's QROLL rebuilt on this run's panels (its SMALL439 is")
    log("  gone, so U56/B136 are the comparable rows).")

    # =========================================================== [5] rule 8 on the claim
    log("\n" + "=" * 185)
    log("[5] Q5a - RULE 8 ON THE CLAIM ITSELF (excess measured IS only, read once on 2017+)")
    cl = []
    for fam, sub in ex.groupby("family"):
        cl.append(dict(family=fam, prior=fam in PRIOR_FAMS, n=len(sub),
                       med_IS=sub["excess_IS"].median(), med_OOS=sub["excess_OOS"].median(),
                       pos_IS=float((sub["excess_IS"] > 0).mean()),
                       pos_OOS=float((sub["excess_OOS"] > 0).mean()),
                       rho_IS_OOS=spearman(sub["excess_IS"], sub["excess_OOS"]),
                       rho_rate_IS=spearman(sub["on_share"], sub["excess_IS"]),
                       rho_rate_OOS=spearman(sub["on_share"], sub["excess_OOS"]),
                       sign_agree=float(np.sign(sub["excess_IS"]).eq(
                           np.sign(sub["excess_OOS"])).mean())))
    cl = pd.DataFrame(cl)
    log(cl.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    log("\n  K=5 equal-count bucket curves, IS window then OOS window:")
    for col in ("excess_IS", "excess_OOS"):
        e5b = ex.copy()
        e5b["bk"] = bucket(e5b["on_share"], 5, "count")
        log(f"  {col}:")
        log(e5b.pivot_table(index="family", columns="bk", values=col,
                            aggfunc="median").to_string(float_format=lambda x: f"{x:+.4f}"))

    # =========================================================== [6] rule 8 on the books
    log("\n" + "=" * 185)
    log("[6] Q5b - PROTOCOL KEEP PATHS AND THE RULE-8 BOOK LEG")
    gc["both"] = gc["p4a"] & gc["p4b"]
    kp = gc.groupby(["rung", "gross"]).agg(n=("p4a", "size"), pass4a=("p4a", "sum"),
                                           pass4b=("p4b", "sum"), both=("both", "sum"),
                                           p4a_oos=("p4a_oos", "sum"), p4b_oos=("p4b_oos", "sum"))
    log("  KEEP paths on every gated grid point (4a vs RULES v2, 4b vs SPY):")
    log(kp.to_string())
    log("\n  4b passes at the protocol rung by panel x family:")
    hh2 = gc[gc["rung"] == RUNG_HEAD]
    log(hh2.pivot_table(index="family", columns="panel", values="p4b",
                        aggfunc="sum").to_string())
    log("  binding 4b leg on failure (head rung):")
    log(hh2["fail4b"].value_counts().head(12).to_string())

    log("\n  Rule 8: (level, w) chosen on IS Sharpe 2009-2016 alone, per panel x family x depth "
        "x cadence x gross x rung; OOS read ONCE.")
    picks = []
    gkey = ["panel", "family", "prior", "depth", "cadence", "gross", "rung"]
    for k, sub in gc.groupby(gkey):
        b = sub.loc[sub["IS_Sharpe"].idxmax()]
        mrow = meta[k[0]]
        picks.append(dict(zip(gkey, k)) | dict(
            level=b["level"], w=b["w"], IS_Sharpe=b["IS_Sharpe"], OOS_CAGR=b["OOS_CAGR"],
            OOS_Sharpe=b["OOS_Sharpe"], OOS_MaxDD=b["OOS_MaxDD"],
            base_OOS_Sharpe=mrow["base_rows"][k[6]]["OOS_Sharpe"],
            base_OOS_CAGR=mrow["base_rows"][k[6]]["OOS_CAGR"],
            base_OOS_MaxDD=mrow["base_rows"][k[6]]["OOS_MaxDD"],
            spy_OOS_Sharpe=mrow["spy_row"]["OOS_Sharpe"], spy_OOS_CAGR=mrow["spy_row"]["OOS_CAGR"],
            spy_OOS_MaxDD=mrow["spy_row"]["OOS_MaxDD"],
            p4a=b["p4a"], p4b=b["p4b"], p4a_oos=b["p4a_oos"], p4b_oos=b["p4b_oos"],
            full_CAGR=b["CAGR"], full_Sharpe=b["Sharpe"], full_MaxDD=b["MaxDD"],
            H1=b["H1"], H2=b["H2"], fail4b=b["fail4b"]))
    picks = pd.DataFrame(picks)
    log(f"  {len(picks)} rule-8 picks. Pass rates: 4a full {picks['p4a'].mean():.4f}, "
        f"4b full {picks['p4b'].mean():.4f}, 4a OOS {picks['p4a_oos'].mean():.4f}, "
        f"4b OOS {picks['p4b_oos'].mean():.4f}")
    log("\n  OOS means by family (rung 10 only), pick vs RULES v2 vs SPY:")
    p10 = picks[picks["rung"] == RUNG_HEAD]
    log(p10.groupby(["panel", "family"])[
        ["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "base_OOS_Sharpe", "spy_OOS_Sharpe"]].mean()
        .to_string(float_format=lambda x: f"{x:+.4f}"))
    log(f"\n  picks beating RULES v2 OOS Sharpe: "
        f"{int((p10['OOS_Sharpe'] > p10['base_OOS_Sharpe']).sum())} of {len(p10)};  beating SPY "
        f"OOS Sharpe: {int((p10['OOS_Sharpe'] > p10['spy_OOS_Sharpe']).sum())} of {len(p10)}")

    # ---- [6c] THE GROSS-MATCHED CONTROL: idea 596's bar, the one 4b structurally cannot see
    log("\n" + "=" * 185)
    log("[6c] THE GROSS-MATCHED CONTROL - does 4b see the GATE, or just the EXPOSURE it leaves?")
    log("  Every gated arm's twin is the UNGATED book at the arm's own realised mean gross, so")
    log("  a 4b pass that the twin also earns is a statement about exposure, not about timing.")
    log("\n  First, the UNGATED book itself (no gate, nothing tuned), 4b at every gross x rung:")
    ng = []
    for pname, px in panels.items():
        st = pd.Timestamp(meta[pname]["start"])
        spk = pack_of(px["SPY"].pct_change().fillna(0).loc[st:])
        for g in GROSSES:
            res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
            r0, t0 = res["returns"].loc[st:], res["turnover"].loc[st:]
            for c in RUNGS:
                r = r0 - t0 * c / 1e4
                m = metrics(r)
                t = tests_4b(r, spk)
                ng.append(dict(panel=pname, gross=g, rung=c, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                               MaxDD=m["MaxDD"], p4b=all(t.values()),
                               fail=",".join(k for k, v in t.items() if not v) or "-"))
    ng = pd.DataFrame(ng)
    log(ng.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ng.to_csv(OUT / f"{STEM}.nogate.csv", index=False)

    ctl = []
    for pname, px in panels.items():
        sub = gc[(gc["panel"] == pname) & gc["p4b"]]
        if not len(sub):
            continue
        st = pd.Timestamp(meta[pname]["start"])
        spy = px["SPY"].pct_change().fillna(0).loc[st:]
        spk = pack_of(spy)
        so = spy.loc[OOS_START:]
        m_so = metrics(so)
        so1, so2 = half_sharpes(so)
        sopk = (so1, so2, m_so["MaxDD"], m_so["CAGR"])
        tw = Twins(px, st)
        tw.prewarm(sorted(set(sub["g_eff"].round(6))))
        for _, r in sub.iterrows():
            rt = tw.at(float(r["g_eff"]), int(r["rung"]))
            t = tests_4b(rt, spk)
            ctl.append(dict(panel=pname, rung=int(r["rung"]), family=r["family"],
                            prior=r["prior"], gross=r["gross"], depth=r["depth"],
                            cadence=r["cadence"], level=r["level"], w=r["w"],
                            arm_Sharpe=r["Sharpe"], twin_Sharpe=metrics(rt)["Sharpe"],
                            arm_MaxDD=r["MaxDD"], twin_MaxDD=metrics(rt)["MaxDD"],
                            arm_p4b_oos=r["p4b_oos"], twin_p4b=all(t.values()),
                            twin_p4b_oos=all(tests_4b_window(rt.loc[OOS_START:], sopk).values()),
                            beats_twin=bool(r["dSharpe"] > TIE)))
    ctl = pd.DataFrame(ctl)
    if len(ctl):
        ctl["clean"] = ctl["beats_twin"] & ~ctl["twin_p4b"]
        ctl["both_win"] = ctl["arm_p4b_oos"] & ctl["beats_twin"] & ~ctl["twin_p4b"]
        log(f"  {len(ctl)} 4b passers priced against their own twin, all rungs:")
        log(ctl.groupby(["rung", "panel"]).agg(
            n=("clean", "size"), twin_also_4b=("twin_p4b", "sum"),
            beats_twin=("beats_twin", "sum"), clean=("clean", "sum"),
            clean_and_oos=("both_win", "sum")).to_string())
        log("\n  at the PROTOCOL rung by family:")
        c10 = ctl[ctl["rung"] == RUNG_HEAD]
        log(c10.groupby(["family", "prior"]).agg(
            n=("clean", "size"), twin_also_4b=("twin_p4b", "sum"),
            beats_twin=("beats_twin", "sum"), clean=("clean", "sum"),
            clean_and_oos=("both_win", "sum")).to_string())
        log(f"\n  HEADLINE CONTROL NUMBER: of {len(c10)} arms passing 4b at {RUNG_HEAD} bps, "
            f"{int(c10['twin_p4b'].sum())} have a gross-matched twin that passes 4b TOO; "
            f"{int(c10['clean'].sum())} beat their twin AND have a twin 4b rejects.")
        ctl.to_csv(OUT / f"{STEM}.control.csv", index=False)

    # ---- the single best full-sample 4b arm at the protocol rung, if any
    cand = hh2[hh2["p4b"]].sort_values("Sharpe", ascending=False)
    log("\n  Full-sample 4b passers at the protocol rung (top 12 by Sharpe):")
    if len(cand):
        log(cand[["panel", "family", "level", "w", "depth", "cadence", "gross", "CAGR", "Sharpe",
                  "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "p4b_oos",
                  "dSharpe"]].head(12).to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
        log(f"  of these, {int(cand['p4b_oos'].sum())} also pass 4b read inside the OOS window; "
            f"{int((cand['family'].isin(PRIOR_FAMS)).sum())} of {len(cand)} are prior-direction "
            f"arms.")
        best = cand.iloc[0]
        mrow = meta[best["panel"]]
        log(f"\n  BEST 4b arm: {best['panel']} {best['family']} q{best['level']} w{int(best['w'])} "
            f"d{best['depth']:.2f} {best['cadence']} g{best['gross']:.2f} @{RUNG_HEAD}bps")
        log(f"    full  {best['CAGR']:.2%} / {best['Sharpe']:.3f} / {best['MaxDD']:.2%}  "
            f"H {best['H1']:.3f}/{best['H2']:.3f}")
        log(f"    OOS   {best['OOS_CAGR']:.2%} / {best['OOS_Sharpe']:.3f} / {best['OOS_MaxDD']:.2%}")
        b10 = mrow["base_rows"][RUNG_HEAD]
        log(f"    RULES v2  {b10['CAGR']:.2%} / {b10['Sharpe']:.3f} / {b10['MaxDD']:.2%}  "
            f"OOS {b10['OOS_CAGR']:.2%} / {b10['OOS_Sharpe']:.3f} / {b10['OOS_MaxDD']:.2%}")
        sr = mrow["spy_row"]
        log(f"    SPY       {sr['CAGR']:.2%} / {sr['Sharpe']:.3f} / {sr['MaxDD']:.2%}  "
            f"OOS {sr['OOS_CAGR']:.2%} / {sr['OOS_Sharpe']:.3f} / {sr['OOS_MaxDD']:.2%}")
        log(f"    vs its OWN matched-gross twin: dSharpe {best['dSharpe']:+.4f} "
            f"(twin Sharpe {best['twin_Sharpe']:.3f}) - the gate is "
            f"{'earning' if best['dSharpe']>0 else 'NOT earning'} its exposure.")
        log(f"    was it a rule-8 pick? "
            f"{bool(((picks['panel']==best['panel']) & (picks['family']==best['family']) & (picks['rung']==RUNG_HEAD) & (picks['gross']==best['gross']) & (picks['depth']==best['depth']) & (picks['cadence']==best['cadence']) & (picks['level']==best['level']) & (picks['w']==best['w'])).any())}")
    else:
        log("  NONE.")

    # =========================================================== [7] verdict
    log("\n" + "=" * 185)
    log("[7] VERDICT")
    br = summ[summ["family"] == "BREADTH-LO"].iloc[0]
    log(f"  BREADTH-LO (idea 602's family, rebuilt): {int(br['passes'])} of {int(br['readings'])} "
        f"readings pass the pre-registered slope bar, median rho {br['rho_med']:+.4f}, "
        f"median span {br['span_med']:+.4f}")
    for _, r in summ[summ["family"] != "BREADTH-LO"].iterrows():
        log(f"  {r['family']:<12} {'(prior)' if r['prior'] else '(reversed)':<11} "
            f"{int(r['passes'])} of {int(r['readings'])} readings pass, median rho "
            f"{r['rho_med']:+.4f}, median span {r['span_med']:+.4f}")
    nonb = summ[~summ["family"].str.startswith("BREADTH")]
    log(f"\n  NON-BREADTH families passing at least one reading: "
        f"{int((nonb['passes'] > 0).sum())} of {len(nonb)}; passing ALL ten: "
        f"{int((nonb['passes'] == nonb['readings']).sum())}")

    # =========================================================== [8] the candidate, standalone
    log("\n" + "=" * 185)
    log("[8] THE BOOK THIS GRID THREW UP, REBUILT FROM SCRATCH (no grid machinery, no twin cache)")
    log("  POST-HOC: this cell was read off a 3,456-cell grid built to answer a different")
    log("  question, so it is a KEEP-CANDIDATE and NOT a KEEP.  It is reported because it is the")
    log("  only arm that survives all four of: 4b full, 4b OOS, the rule-8 (level, w) chooser,")
    log("  and a gross-matched twin that 4b itself REJECTS - and it is a NON-BREADTH gate.")
    if len(ctl):
        cln = ctl[(ctl["rung"] == RUNG_HEAD) & ctl["clean"] & ctl["arm_p4b_oos"]]
        pk = picks[picks["rung"] == RUNG_HEAD][["panel", "family", "depth", "cadence", "gross",
                                                "level", "w"]].assign(is_pick=True)
        cln = cln.merge(pk, on=["panel", "family", "depth", "cadence", "gross", "level", "w"],
                      how="left")
        cln["is_pick"] = cln["is_pick"].fillna(False)
        c25 = ctl[(ctl["rung"] == 25) & ctl["clean"] & ctl["arm_p4b_oos"]][
            ["panel", "family", "depth", "cadence", "gross", "level", "w"]].assign(ok25=True)
        cln = cln.merge(c25, on=["panel", "family", "depth", "cadence", "gross", "level", "w"],
                      how="left")
        cln["ok25"] = cln["ok25"].fillna(False)
        log(f"  clean 4b passers (beat their twin AND their twin fails 4b) that also pass 4b OOS: "
            f"{len(cln)};  of those, rule-8 IS picks: {int(cln['is_pick'].sum())};  still clean at "
            f"25 bps: {int(cln['ok25'].sum())};  BOTH: {int((cln['is_pick'] & cln['ok25']).sum())}")
        log(cln.groupby(["family", "prior"]).agg(n=("is_pick", "size"), rule8=("is_pick", "sum"),
                                                at25=("ok25", "sum")).to_string())
        log("\n  the survivors of all four filters:")
        log(cln[cln["is_pick"] & cln["ok25"]][
            ["panel", "family", "level", "w", "depth", "cadence", "gross", "arm_Sharpe",
             "arm_MaxDD", "twin_Sharpe", "twin_MaxDD"]].to_string(
            index=False, float_format=lambda x: f"{x:+.4f}"))
        cln.to_csv(OUT / f"{STEM}.clean.csv", index=False)

    # the named candidate, rebuilt with nothing but baseline.py + engine
    CAND = dict(panel="B136", q=0.17, w=252, depth=0.50, cadence="D", gross=1.00)
    px = panels[CAND["panel"]]
    st = pd.Timestamp(meta[CAND["panel"]]["start"])
    cs = state_corr(px)
    th = cs.rolling(CAND["w"], min_periods=CAND["w"]).quantile(1 - CAND["q"])
    m = gate_mult(cs, th, "HI", CAND["depth"], CAND["cadence"], px.index)
    res = backtest(px, ewall_weights(px, CAND["gross"]), cost_bps=0, freq=FREQ)
    r0, t0 = res["returns"].loc[st:], res["turnover"].loc[st:]
    me = m.reindex(r0.index).shift(1).fillna(1.0)

    def cand_at(c, lag=1):
        mm = m.reindex(r0.index).shift(lag).fillna(1.0)
        return mm * (r0 - t0 * c / 1e4) - mm.diff().abs().fillna(0.0) * CAND["gross"] * c / 1e4

    spy = px["SPY"].pct_change().fillna(0).loc[st:]
    spk = pack_of(spy)
    rows = [("CANDIDATE CORR-HI q0.17 w252 d0.50 D g1.00", cand_at(RUNG_HEAD)),
            ("RULES v2 baseline (live)",
             backtest(px, rules_v2_weights(px), cost_bps=RUNG_HEAD, freq=FREQ)["returns"].loc[st:]),
            ("RULES v1 (previous)",
             backtest(px, rules_v1_weights(px), cost_bps=RUNG_HEAD, freq=FREQ)["returns"].loc[st:]),
            ("SPY", spy),
            ("ungated EWALL g=1.00 (the gate removed)", r0 - t0 * RUNG_HEAD / 1e4)]
    tbl = []
    for nm, r in rows:
        mm = metrics(r)
        h1, h2 = half_sharpes(r)
        mo = metrics(r.loc[OOS_START:])
        tbl.append(dict(name=nm, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                        H1=h1, H2=h2, IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    tbl = pd.DataFrame(tbl).set_index("name")
    log(tbl.to_string(float_format=lambda x: f"{x:.4f}"))
    a, sp, bl = tbl.iloc[0], tbl.loc["SPY"], tbl.loc["RULES v2 baseline (live)"]
    log(f"\n  4b legs: H1 {a.H1:.3f}>{sp.H1:.3f} {a.H1>sp.H1} | H2 {a.H2:.3f}>{sp.H2:.3f} "
        f"{a.H2>sp.H2} | OOS {a.OOS_Sharpe:.3f}>{sp.OOS_Sharpe:.3f} {a.OOS_Sharpe>sp.OOS_Sharpe} "
        f"| DD {a.MaxDD:.2%} <= {-0.6*abs(sp.MaxDD):.2%} {abs(a.MaxDD)<=0.6*abs(sp.MaxDD)} "
        f"| CAGR {a.CAGR:.2%} >= {0.7*sp.CAGR:.2%} {a.CAGR>=0.7*sp.CAGR}  -> 4b PASS")
    log(f"  4a legs: H1 {a.H1:.3f}>{bl.H1:.3f} {a.H1>bl.H1} | H2 {a.H2:.3f}>{bl.H2:.3f} "
        f"{a.H2>bl.H2} | MaxDD {a.MaxDD:.2%} >= {bl.MaxDD:.2%} {a.MaxDD>=bl.MaxDD}  -> 4a FAIL "
        f"(the standing result: no growth book reaches the live band book's drawdown)")
    log(f"  firing rate {float((me<1.0).mean()):.4f} of days, mean gross {float(me.mean()):.4f}, "
        f"ungated turnover {t0.sum()/(len(r0)/252):.2f}x/yr")
    log("\n  cost ladder and execution-lag ladder (4b re-read at every point):")
    for c in [0, 5, 10, 25, 50]:
        r = cand_at(c)
        mm, mo = metrics(r), metrics(r.loc[OOS_START:])
        ok = all(tests_4b(r, spk).values())
        log(f"    cost {c:>2} bps: {mm['CAGR']:.2%} / {mm['Sharpe']:.3f} / {mm['MaxDD']:.2%}   "
            f"OOS {mo['CAGR']:.2%} / {mo['Sharpe']:.3f} / {mo['MaxDD']:.2%}   4b={ok}")
    for lag in [1, 2, 3]:
        r = cand_at(RUNG_HEAD, lag)
        mm, mo = metrics(r), metrics(r.loc[OOS_START:])
        ok = all(tests_4b(r, spk).values())
        log(f"    lag {lag} day(s) @{RUNG_HEAD} bps: {mm['CAGR']:.2%} / {mm['Sharpe']:.3f} / "
            f"{mm['MaxDD']:.2%}   OOS {mo['Sharpe']:.3f}   4b={ok}")
    log("\n  SURVIVORSHIP: B136 is universe_broad.json, current constituents, so the LEVELS are")
    log("  optimistic for every row in the table above, the SPY bars included.")

    # ---- writes
    gc.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    ex.to_csv(OUT / f"{STEM}.excess.csv", index=False)
    sl.to_csv(OUT / f"{STEM}.slope.csv", index=False)
    picks.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    gates.to_csv(OUT / f"{STEM}.gates.csv", index=False)
    cl.to_csv(OUT / f"{STEM}.claim.csv", index=False)
    ph.to_csv(OUT / f"{STEM}.placebo.csv.gz", index=False, compression="gzip")
    log(f"\n  wrote {STEM}.{{cells,excess,slope,walkforward,gates,claim}}.csv "
        f"+ .placebo.csv.gz  ({time.time()-T0:.0f}s)")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 609 - "is-the-TWIN-ORDERING-window-invariant-on-a-ROLLING-census" (lane B, 2026-09-12).

INDEPENDENT THIRD RUN, FILED AS A REPLICATION, NOT A CLAIM.  Idea 609 was already answered and
committed twice while this run was executing: aa87884 (lane B, headline WINDOW-matched twin,
0.0847) and 2c96cad (cloud, headline FULL-matched twin, 0.322).  This script was written without
sight of either, from idea 605's committed outputs alone.  It is committed under the _B2 suffix so
it clobbers neither, and its value is adjudication: it reproduces the cloud run's FULL-matched
headline EXACTLY on an independent implementation (19 of 59 windows, 0.322034; QROLL on top
0.644068; cost ladder 0.271186 / 0.322034 / 0.305085 at 0 / 10 / 25 bps), and it extends the
census from 9 (window, step) points to 75 and from 59 windows to 176, so the shared verdict is
shown not to be an artefact of the step-63 sampling both prior runs used.  It uses idea 605's
FULL-matched twin throughout; the WINMATCH convention that produced aa87884's 0.0847 was
separately diagnosed in 7df829b (lane C).

The finding this run exists to price
------------------------------------
Idea 605 published the MATCHED-MEAN-GROSS STATIC TWIN win rate for three gate families and found
the ordering QROLL > QEXP > ABS at every one of 15 cost rungs (Spearman vs the c=0 order +1.000
at all 15).  It then filed ONE caveat against itself, in its own words:

    "the *ordering* is cost-invariant but **not window-invariant.**  Ranked on the IS window alone
     the families read ABS < QROLL < QEXP; on OOS they read QEXP < ABS < QROLL (rho -0.500).  The
     full-sample ordering QROLL > QEXP > ABS holds at all 15 rungs; the half-window orderings
     disagree with each other."

Two windows is two draws.  A reader of the record does not get the full sample - they get whatever
window they are standing in.  This run turns the caveat into a census: re-rank the three families
on a ROLLING window and report HOW OFTEN the published full-sample order is the one a reader would
actually have seen, at every window length, every step, and every cost rung.

The question, stated so it can be answered either way
-----------------------------------------------------
    Q1 (AGREEMENT)   THE DECIDING TEST.  Over rolling windows, what share show the published strict
                     order QROLL > QEXP > ABS?  Pre-registered bar H1: >= 0.80 at the headline
                     cell (3-year window, monthly step, PROTOCOL's 10 bps) means the published
                     ordering is what a reader sees and the caveat is a two-draw artefact; below
                     0.80 means the published ordering is a full-sample statement only.
    Q2 (WHICH LEG)   Which of the three pairwise legs breaks?  H2: QROLL tops >= 0.90 of windows.
                     H3: ABS is bottom in >= 0.80 of windows.  The IS/OOS disagreement idea 605
                     reported is entirely a QEXP-vs-ABS story if H2 and H3 both hold.
    Q3 (PARAMS)      H4: the agreement rate moves < 0.15 across the five window lengths at fixed
                     step.  H5: it moves < 0.05 across the three steps at fixed length (step
                     changes only sampling density, not content - a bar this run should pass
                     trivially, and a failure would mean the census is aliasing).
    Q4 (COST)        H6: idea 605's cost-invariance is a WITHIN-WINDOW fact too - in >= 0.90 of
                     windows the family order at 0 bps equals the order at 100 bps.
    Q5 (RULE 8)      H7: the family that tops the most IS (<=2016) windows also tops the most OOS
                     (2017+) windows.  And the capital leg PROTOCOL rule 8 requires: pick ONE book
                     on IS alone by the rolling census, read it ONCE on OOS, report OOS CAGR /
                     Sharpe / MaxDD against RULES v2, RULES v1 and SPY.  H8: that book passes 4b.
    Q6 (PROTOCOL)    Both KEEP paths on EVERY one of the 9 720 grid points (648 twin pairs x 15
                     cost rungs), reported in full, never selected on.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both, and only these two
    1. window   378 / 504 / 756 / 1008 / 1260 trading days (1.5 / 2 / 3 / 4 / 5 yrs).  The queue
                says "3-year", so 756 is the HEADLINE, declared before the run; all five reported.
    2. step     21 / 63 / 126 trading days.  Headline 21 (monthly); all three reported.

Reported axes, NEVER tuned and NEVER selected on (inherited verbatim from ideas 602/605 so the
population is literally the same one, and reproduced field-for-field in gate G3)
    family   ABS(B in 0.30/0.40/0.50) / QEXP(q) / QROLL(q, w)
    q        0.07 / 0.12 / 0.17      w  252 / 504 / 1008 / 2016
    depth    0.25 / 0.50 / 1.00      panel  U56 / B136 / SMALL439      gross  0.75 / 1.00
    cost     15 rungs 0 -> 100 bps.  Idea 605 made cost a TUNED axis; here it is a reported axis,
             because 605 already showed the ordering is cost-invariant full-sample, so cost cannot
             be a selector for this run.  PROTOCOL's 10 bps is the headline rung.

Reproduction gates (section [0], printed before any new number is read)
    G1  the derived cost ladder r_gate(c) = m*r0 - (c/1e4)*(m*t0 + g*|dm|) against a LIVE
        engine.backtest put through idea 399's apply_gate, at every rung.
    G2  fast numpy metrics (CAGR / Sharpe / MaxDD) vs engine.metrics on 200 real series.
    G3  idea 605's COMMITTED .cells.csv.gz, all 9 720 gated rows joined field-for-field on
        (panel, rung, gross, family, level, w, depth, cadence), plus its .ordering.csv headline.
        G3 IS REPORTED PER PANEL, because it does not pass on all three - see below.

    THE SMALL PANEL IS NOT THE RECORD'S SMALL439 ANY MORE (found by G3, before any new number
    was read).  `data/prices_small.csv.gz` is rewritten by the daily Actions job; the commit
    "Daily close 2026-09-11 [actions]" (56e08b1, 2026-09-11 23:27 UTC) took it from 483 columns
    to 715, i.e. from idea 605's 439 names + SPY to 663 names + SPY.  Every panel statistic the
    record files under the label "SMALL439" from that commit onward is a different panel under an
    old name.  This run therefore calls it SMALL<n> by its measured width, reproduces U56 and B136
    against idea 605 row for row, and publishes the census on BOTH the three-panel population
    (as pre-declared) and the two reproducing panels, so no headline rests on the swap.
    G4  idea 84's ungated EWALL U56 g=0.85 @10bps: 11.8% / 1.05 / -17.9%.
    G5  the O(1) cumsum window-Sharpe against a direct fsharpe on the same slice, one random
        (arm, rung, window) triple per twin pair (648 of them).  The census rests on this identity.

Data: committed caches only, no network, never yfinance.  SURVIVORSHIP: all three panels are
current-constituent lists, so CAGR and drawdown LEVELS are optimistic; the gate-minus-twin
contrast and its window census are the durable part.  SMALL439 starts 2010-01-04, so it enters
only the windows its own calendar covers (>= 90% of the window's days), and that coverage is
printed per cell rather than assumed.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import sys
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
PARENT_ORDER = OUT / "2026-09-10_is-the-TWIN-WIN-RATE-a-SWITCHING-COST-statistic_C.ordering.csv"
PARENT_CELLS = OUT / "2026-09-10_is-the-TWIN-WIN-RATE-a-SWITCHING-COST-statistic_C.cells.csv.gz"
PARENT_SMALL = "SMALL439"          # idea 605's label for the panel this cache used to hold

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 1.00]
G_HEAD = 0.75
QS = [0.07, 0.12, 0.17]
BS = [0.30, 0.40, 0.50]
WS = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
RUNGS = [0.0, 1.0, 2.0, 3.0, 5.0, 7.5, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 75.0, 100.0]
RUNG_HEAD = 10.0
MINQ = 252
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TIE = 1e-12                       # ideas 594/595: a tie is NOT a win

WINDOWS = [378, 504, 756, 1008, 1260]      # tuned param 1
STEPS = [21, 63, 126]                      # tuned param 2
W_HEAD, S_HEAD = 756, 21                   # declared before the run (the queue says "3-year")
COVER = 0.90                               # a panel joins a window only if it covers >= 90% of it
FAMS = ["ABS", "QEXP", "QROLL"]
PUB_ORDER = ("QROLL", "QEXP", "ABS")       # idea 605's published full-sample order, top -> bottom

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)

LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


# ---------------------------------------------------------------- primitives (idea 42/336/399)
_ELIG = {}


def eligible_mask(px):
    k = (id(px), px.shape, px.index[0], px.index[-1])
    if k not in _ELIG:
        _, above, vol20 = score(px)
        _ELIG[k] = above & (vol20 < MAX_VOL)
    return _ELIG[k]


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def _cadence(m, idx):
    mask = rebalance_mask(idx, FREQ)
    return m.where(mask).ffill().fillna(1.0)


def gate_from_thr(br, thr, depth, cadence, idx):
    m = pd.Series(1.0, index=idx).where(~(br < thr), 1.0 - depth)
    m = m.where(br.notna() & thr.notna(), 1.0)
    return _cadence(m, idx) if cadence == "W" else m


def gate_abs(br, B, depth, cadence, idx):
    m = pd.Series(1.0, index=idx).where(~(br < B), 1.0 - depth)
    m = m.where(br.notna(), 1.0)
    return _cadence(m, idx) if cadence == "W" else m


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


# ---------------------------------------------------------------- fast metrics (G2)
def fmet(r):
    n = len(r)
    if n < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    yrs = n / 252.0
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    dd = (eq / np.maximum.accumulate(eq) - 1.0).min()
    vol = r.std(ddof=1) * np.sqrt(252.0)
    sh = (r.mean() * 252.0) / vol if vol else np.nan
    return cagr, sh, dd


def fsharpe(r):
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def rows_metrics(R):
    """(CAGR, Sharpe, MaxDD) for every row of a (k, n) matrix, identical to fmet row-wise."""
    n = R.shape[1]
    eq = np.cumprod(1.0 + R, axis=1)
    cagr = eq[:, -1] ** (252.0 / n) - 1.0
    dd = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
    vol = R.std(axis=1, ddof=1) * np.sqrt(252.0)
    sh = np.where(vol > 0, R.mean(axis=1) * 252.0 / np.where(vol > 0, vol, 1.0), np.nan)
    return cagr, sh, dd


def rows_sharpe(R):
    vol = R.std(axis=1, ddof=1) * np.sqrt(252.0)
    return np.where(vol > 0, R.mean(axis=1) * 252.0 / np.where(vol > 0, vol, 1.0), np.nan)


def win_sharpe(cs, cs2, i, j):
    """Sharpe of r[i:j] for every row, from cumulative sums.  cs/cs2 are (k, n+1).  O(1) per
    window; gate G5 prices it against a direct fsharpe on the same slice."""
    n = (j - i).astype(float)
    s1 = cs[:, j] - cs[:, i]
    s2 = cs2[:, j] - cs2[:, i]
    mean = s1 / n
    var = (s2 - n * mean * mean) / (n - 1.0)
    var = np.where(var > 0, var, np.nan)
    return mean * 252.0 / (np.sqrt(var) * np.sqrt(252.0))


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.rank().corr(b.rank()))


class Slices:
    def __init__(self, idx):
        self.n = len(idx)
        self.h = self.n // 2
        self.is_end = int(idx.searchsorted(pd.Timestamp(IS_END), side="right"))
        self.oos = int(idx.searchsorted(pd.Timestamp(OOS_START), side="left"))


# ---------------------------------------------------------------- twin machinery (idea 602/605)
GSTEP = 0.01


class Twins:
    """Static-gross EWALL twin (returns, turnover) at cost 0, exact g by linear interpolation on a
    GSTEP cache (idea 602's G4 priced the interpolation error at <= 4e-07 of Sharpe)."""

    def __init__(self, px, start):
        self.px, self.start = px, start
        self.cache = {}
        self.n_bt = 0

    def _exact(self, g):
        g = round(g, 6)
        if g not in self.cache:
            res = backtest(self.px, ewall_weights(self.px, g), cost_bps=0, freq=FREQ)
            self.cache[g] = (res["returns"].loc[self.start:].values,
                             res["turnover"].loc[self.start:].values)
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

    def at0(self, g):
        lo = round(np.floor(round(g, 6) / GSTEP) * GSTEP, 6)
        lam = (round(g, 6) - lo) / GSTEP
        if lam <= 1e-9:
            return self._exact(lo)
        rl, tl = self._exact(lo)
        rh, th = self._exact(round(lo + GSTEP, 6))
        return (1 - lam) * rl + lam * rh, (1 - lam) * tl + lam * th


# ---------------------------------------------------------------- census bookkeeping
def order_of(vals):
    """Strict top->bottom ordering of the three families, or None if any tie/NaN."""
    v = [vals[f] for f in FAMS]
    if any(not np.isfinite(x) for x in v):
        return None
    if len(set(v)) < 3:
        return None
    return tuple(sorted(FAMS, key=lambda f: -vals[f]))


RUNG_ARR = np.array(RUNGS)
RUNG_IX = {c: i for i, c in enumerate(RUNGS)}
HEAD_IX = RUNG_IX[RUNG_HEAD]


def run_panel(panel, px, master_idx, win_defs):
    """Returns (per-arm grid rows, per-(W,S,rung,window) family win/total tensors)."""
    start = px.index[260]
    idx = px.index
    eval_idx = px.loc[start:].index
    S = Slices(eval_idx)
    spy = px["SPY"].pct_change().fillna(0).loc[start:].values
    sc, ss, sd = fmet(spy)
    spy_h1, spy_h2 = fsharpe(spy[:S.h]), fsharpe(spy[S.h:])
    spy_oos_c, spy_oos_s, spy_oos_d = fmet(spy[S.oos:])

    br_full = breadth(px)
    br = br_full.loc[start:]
    log(f"\n{'='*190}\nPANEL {panel}: {px.shape[1]} columns, {idx[0].date()} -> {idx[-1].date()}, "
        f"eval from {start.date()} ({len(eval_idx)} days)")
    log(f"  SPY {sc:.2%} / {ss:.3f} / {sd:.2%}; 4b bars CAGR floor {0.70*sc:.2%}, DD cap "
        f"{-0.60*abs(sd):.2%}, halves {spy_h1:.3f}/{spy_h2:.3f}, OOS {spy_oos_s:.3f}")

    thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
    thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q) for q in QS for w in WS}

    base0 = {}
    for g in GROSSES:
        res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
        base0[g] = (res["returns"].loc[start:].values, res["turnover"].loc[start:].values)
    rv2 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
    rv1 = backtest(px, rules_v1_weights(px), cost_bps=0, freq=FREQ)
    ref0 = {"v2": (rv2["returns"].loc[start:].values, rv2["turnover"].loc[start:].values),
            "v1": (rv1["returns"].loc[start:].values, rv1["turnover"].loc[start:].values)}
    base_packs = {}
    for c in RUNGS:                                   # RULES v2 bars for path 4a, per rung
        b = ref0["v2"][0] - ref0["v2"][1] * c / 1e4
        base_packs[c] = (fsharpe(b[:S.h]), fsharpe(b[S.h:]), fmet(b)[2])

    arms = ([("ABS", B, 0) for B in BS] + [("QEXP", q, 0) for q in QS]
            + [("QROLL", q, w) for q in QS for w in WS])
    m_eff, switch, on_share = {}, {}, {}
    for fam, lev, w in arms:
        thr = None if fam == "ABS" else (thr_exp[lev] if fam == "QEXP" else thr_roll[(lev, w)])
        for d, cad in product(DEPTHS, CADENCES):
            m = (gate_abs(br_full, lev, d, cad, idx) if fam == "ABS"
                 else gate_from_thr(br_full, thr, d, cad, idx))
            me = m.reindex(eval_idx).shift(1).fillna(1.0).values
            m_eff[(fam, lev, w, d, cad)] = me
            switch[(fam, lev, w, d, cad)] = np.abs(np.diff(me, prepend=me[0]))
            on_share[(fam, lev, w, d, cad)] = float((me < 1.0).mean())

    tw = Twins(px, start)
    tw.prewarm([g * float(m_eff[(f, l, w, d, cad)].mean())
                for (f, l, w), (d, cad), g in
                product(arms, product(DEPTHS, CADENCES), GROSSES)])
    log(f"  twin gross cache: {tw.n_bt} backtests on a {GSTEP} grid spanning "
        f"{min(tw.cache):.2f}-{max(tw.cache):.2f}")

    # ---- window index arrays for this panel, per (W, S).  A panel joins a window only if its own
    #      calendar covers >= COVER of the window's master-calendar span.
    wmap = {}
    for (W, ST), defs in win_defs.items():
        ii, jj, keep = [], [], []
        for k, (d0, d1) in enumerate(defs):
            i = int(eval_idx.searchsorted(d0, side="left"))
            j = int(eval_idx.searchsorted(d1, side="right"))
            if (j - i) >= COVER * W:
                ii.append(i); jj.append(j); keep.append(k)
        wmap[(W, ST)] = (np.array(ii, int), np.array(jj, int), np.array(keep, int))

    # ---- accumulators: wins[(W,S)][fam] and tot[(W,S)][fam], each (n_rungs, n_master_windows)
    wins = {k: {f: np.zeros((len(RUNGS), len(v)), int) for f in FAMS} for k, v in win_defs.items()}
    tots = {k: {f: np.zeros((len(RUNGS), len(v)), int) for f in FAMS} for k, v in win_defs.items()}

    grid, g5_samples = [], []
    rng = np.random.default_rng(609)
    for g in GROSSES:
        r0, t0 = base0[g]
        for (fam, lev, w), d, cad in product(arms, DEPTHS, CADENCES):
            key = (fam, lev, w, d, cad)
            me, sw = m_eff[key], switch[key]
            g_eff = g * float(me.mean())
            rg0, Cg = me * r0, me * t0 + g * sw
            rs0, Cs = tw.at0(g_eff)
            # (n_rungs, n) matrices: the whole cost ladder, exact
            RG = rg0[None, :] - np.outer(RUNG_ARR, Cg) / 1e4
            RS = rs0[None, :] - np.outer(RUNG_ARR, Cs) / 1e4
            z = np.zeros((len(RUNGS), 1))
            csg, csg2 = np.hstack([z, np.cumsum(RG, axis=1)]), np.hstack([z, np.cumsum(RG ** 2, axis=1)])
            css, css2 = np.hstack([z, np.cumsum(RS, axis=1)]), np.hstack([z, np.cumsum(RS ** 2, axis=1)])

            for (W, ST), (ii, jj, keep) in wmap.items():
                if not len(ii):
                    continue
                dS = win_sharpe(csg, csg2, ii, jj) - win_sharpe(css, css2, ii, jj)
                wins[(W, ST)][fam][:, keep] += (dS > TIE)
                tots[(W, ST)][fam][:, keep] += np.isfinite(dS)

            # G5 sample: one random (rung, window) triple per arm
            if len(wmap[(W_HEAD, S_HEAD)][0]):
                ii, jj, _ = wmap[(W_HEAD, S_HEAD)]
                a = int(rng.integers(len(ii)))
                ri = int(rng.integers(len(RUNGS)))
                g5_samples.append((float(win_sharpe(csg, csg2, ii[a:a+1], jj[a:a+1])[ri, 0]),
                                   float(fsharpe(RG[ri, ii[a]:jj[a]]))))

            # ---- full-sample grid rows: both KEEP paths at every rung
            cg, shg, ddg = rows_metrics(RG)
            h1 = rows_sharpe(RG[:, :S.h]); h2 = rows_sharpe(RG[:, S.h:])
            isS = rows_sharpe(RG[:, :S.is_end])
            ocg, oshg, oddg = rows_metrics(RG[:, S.oos:])
            shs = rows_sharpe(RS)
            oshs = rows_sharpe(RS[:, S.oos:])
            for ri, c in enumerate(RUNGS):
                b1, b2, bdd = base_packs[c]
                t4b = dict(H1=h1[ri] > spy_h1, H2=h2[ri] > spy_h2, OOS=oshg[ri] > spy_oos_s,
                           DD=abs(ddg[ri]) <= 0.60 * abs(sd), CAGR=cg[ri] >= 0.70 * sc)
                grid.append(dict(
                    panel=panel, rung=c, gross=g, family=fam, level=lev, w=w, depth=d, cadence=cad,
                    arm=f"{fam} L{lev:.2f} w{w} d{d:.2f} {cad} g{g:.2f}", g_eff=g_eff,
                    on_share=on_share[key], CAGR=cg[ri], Sharpe=shg[ri], MaxDD=ddg[ri],
                    H1=h1[ri], H2=h2[ri], IS_Sharpe=isS[ri], OOS_CAGR=ocg[ri],
                    OOS_Sharpe=oshg[ri], OOS_MaxDD=oddg[ri], twin_Sharpe=shs[ri],
                    dSharpe=shg[ri] - shs[ri], dOOS=oshg[ri] - oshs[ri],
                    win=bool(shg[ri] - shs[ri] > TIE),
                    p4a=bool(h1[ri] > b1 and h2[ri] > b2 and ddg[ri] >= bdd),
                    p4b=all(t4b.values()),
                    fail4b=",".join([k for k, v in t4b.items() if not v]) or "-"))

    refs = dict(SPY=(sc, ss, sd, spy_h1, spy_h2, spy_oos_c, spy_oos_s, spy_oos_d))
    for g in GROSSES:                                  # ungated references, the G3b calibrators
        ref0[f"NOGATE g{g:.2f}"] = base0[g]
    for nm, (r, t) in ref0.items():
        rr = r - t * RUNG_HEAD / 1e4
        c_, s_, d_ = fmet(rr)
        oc_, os_, od_ = fmet(rr[S.oos:])
        refs[nm] = (c_, s_, d_, fsharpe(rr[:S.h]), fsharpe(rr[S.h:]), oc_, os_, od_)
    return pd.DataFrame(grid), wins, tots, g5_samples, refs, S, eval_idx


def main():
    log("=" * 190)
    log(f"Idea 609 is-the-TWIN-ORDERING-window-invariant-on-a-ROLLING-census (lane B) | {SCRIPT}")
    log("=" * 190)
    log("Base book (fixed, idea 28/42/336/399's): EWALL(G) = equal weight every name above its own")
    log("  200d MA with vol20 < 0.60, at G/E_t, weekly, next-day execution.")
    log("Overlay: carry the book at (1-depth) whenever panel breadth is BELOW the threshold.")
    log("Comparand for EVERY arm: the MATCHED-MEAN-GROSS STATIC TWIN (EWALL at constant g_eff).")
    log(f"Tuned (2): window in {WINDOWS} trading days, step in {STEPS}.  Headline {W_HEAD}/{S_HEAD}"
        f" declared before the run because the queue says '3-year'.")
    log(f"Reported never tuned: cost rung {RUNGS} bps, family, level, w, depth, panel, gross.")
    log(f"Published order under test (idea 605): {' > '.join(PUB_ORDER)}.  Tie bar |dSharpe| <= {TIE:g}.")

    # =================================================================== [0] gates
    log("\n" + "=" * 190)
    log("[0] REPRODUCTION GATES (all printed before any new number is read)")
    px0 = load_universe()
    st0 = px0.index[260]
    idx0 = px0.loc[st0:].index

    res0 = backtest(px0, ewall_weights(px0, G_HEAD), cost_bps=0, freq=FREQ)
    r0 = res0["returns"].loc[st0:].values
    t0 = res0["turnover"].loc[st0:].values
    brf = breadth(px0)
    mtest = gate_abs(brf, 0.40, 0.50, "W", px0.index).reindex(idx0).shift(1).fillna(1.0)
    me = mtest.values
    sw = np.abs(np.diff(me, prepend=me[0]))
    g1 = 0.0
    for c in RUNGS:
        live = backtest(px0, ewall_weights(px0, G_HEAD), cost_bps=c,
                        freq=FREQ)["returns"].loc[st0:].values
        ref = me * live - sw * G_HEAD * c / 1e4
        der = me * r0 - (me * t0 + G_HEAD * sw) * c / 1e4
        g1 = max(g1, float(np.abs(live - (r0 - t0 * c / 1e4)).max()),
                 float(np.abs(ref - der).max()))
    log(f"  G1 derived ladder == live backtest through apply_gate, all {len(RUNGS)} rungs: "
        f"max |diff| = {g1:.3e} (bar 1e-12) -> {'PASS' if g1 < 1e-12 else 'FAIL'}")

    rng = np.random.default_rng(6090)
    g2 = 0.0
    for _ in range(200):
        c = float(rng.uniform(0, 100))
        a, b = sorted(rng.choice(len(r0), 2, replace=False))
        if b - a < 300:
            a, b = 0, len(r0)
        s = pd.Series((r0 - t0 * c / 1e4)[a:b], index=idx0[a:b])
        mm, f = metrics(s), fmet(s.values)
        g2 = max(g2, abs(mm["CAGR"] - f[0]), abs(mm["Sharpe"] - f[1]), abs(mm["MaxDD"] - f[2]))
    log(f"  G2 fast metrics vs engine.metrics on 200 series: max |diff| = {g2:.3e} "
        f"(bar 1e-12) -> {'PASS' if g2 < 1e-12 else 'FAIL'}")

    r84 = backtest(px0, ewall_weights(px0, 0.85), cost_bps=10, freq=FREQ)["returns"].loc[st0:]
    c84, s84, d84 = fmet(r84.values)
    S0 = Slices(idx0)
    log(f"  G4 idea 84 EWALL U56 g=0.85 @10bps: {c84:.2%} / {s84:.3f} / {d84:.2%} "
        f"H {fsharpe(r84.values[:S0.h]):.3f}/{fsharpe(r84.values[S0.h:]):.3f} "
        f"(committed 11.8% / 1.05 / -17.9% / 1.07 / 1.04) -> "
        f"{'PASS' if abs(c84-0.118) < 6e-3 and abs(s84-1.05) < 6e-3 and abs(d84+0.179) < 6e-3 else 'CHECK'}")

    # ================================================================ panels + master calendar
    panels = [("U56", px0), ("B136", load_universe(broad=True))]
    ps, ndrop = small_panel()
    SMALL = f"SMALL{ps.shape[1]-1}"
    panels.append((SMALL, ps))
    log(f"  SMALL panel: idea 399/602/605's construction applied to TODAY's cache -> dropped "
        f"{ndrop} names with max_1d_move >= 1.0, leaving {ps.shape[1]-1} names + SPY, so this "
        f"run calls it {SMALL}.")
    if SMALL != PARENT_SMALL:
        log(f"  !! data/prices_small.csv.gz is rewritten by the daily Actions job and no longer "
            f"holds the record's {PARENT_SMALL} panel.  Commit 56e08b1 'Daily close 2026-09-11 "
            f"[actions]' (2026-09-11 23:27 UTC) took it 483 -> 715 columns.  Idea 605's "
            f"{PARENT_SMALL} rows CANNOT reproduce here and G3 is read per panel accordingly.")

    master = idx0                       # U56's eval calendar is the record's native one
    win_defs = {}
    for W, ST in product(WINDOWS, STEPS):
        defs = [(master[i], master[i + W - 1]) for i in range(0, len(master) - W + 1, ST)]
        win_defs[(W, ST)] = defs
    log(f"  master census calendar: U56 eval index {master[0].date()} -> {master[-1].date()} "
        f"({len(master)} days); windows per (W,step): "
        + ", ".join(f"{W}/{ST}:{len(v)}" for (W, ST), v in sorted(win_defs.items())))

    GRID, WINS, TOTS, G5, REFS, SL, EIDX = [], {}, {}, [], {}, {}, {}
    for name, px in panels:
        grid, wins, tots, g5, refs, S, eidx = run_panel(name, px, master, win_defs)
        GRID.append(grid)
        WINS[name], TOTS[name] = wins, tots
        G5 += g5
        REFS[name], SL[name], EIDX[name] = refs, S, eidx
    grid = pd.concat(GRID, ignore_index=True)

    g5a = np.array([x[0] for x in G5]); g5b = np.array([x[1] for x in G5])
    ok = np.isfinite(g5a) & np.isfinite(g5b)
    g5m = float(np.abs(g5a[ok] - g5b[ok]).max()) if ok.any() else np.nan
    log(f"\n  G5 O(1) cumsum window-Sharpe vs direct fsharpe on the same slice, {int(ok.sum())} "
        f"(arm, rung, window) triples: max |diff| = {g5m:.3e} (bar 1e-9) -> "
        f"{'PASS' if g5m < 1e-9 else 'FAIL'}")

    # ---- G3: join idea 605's committed per-arm cells, PER PANEL
    full = (grid.groupby(["rung", "family"])["win"].mean().unstack())
    g3 = pd.DataFrame()
    repro = []                       # panels that reproduce idea 605 and may carry its claim
    if PARENT_CELLS.exists():
        p_all = pd.read_csv(PARENT_CELLS)
        p605_refs = p_all[p_all["family"].isin(["ref", "NOGATE"])].copy()
        p = p_all[~p_all["family"].isin(["ref", "NOGATE"])].copy()
        mine = grid.copy()
        mine["panel"] = mine["panel"].replace({SMALL: PARENT_SMALL})   # join key only
        key = ["panel", "rung", "gross", "family", "level", "w", "depth", "cadence"]
        for df in (p, mine):
            for k in ("rung", "gross", "level", "w", "depth"):
                df[k] = df[k].astype(float).round(6)
        g3 = mine.merge(p, on=key, suffixes=("", "_605"))
        g3["flip"] = g3["win"] != g3["win_605"]
        for col in ("Sharpe", "twin_Sharpe", "dSharpe", "g_eff", "on_share"):
            g3["d_" + col] = (g3[col] - g3[col + "_605"]).abs()
        log(f"  G3 idea 605 {PARENT_CELLS.name}: {len(g3)} of {len(grid)} rows joined "
            f"field-for-field.  BAR (declared on the statistic this run actually uses, which is a "
            f"SIGN test): per-panel win-flip rate <= 0.01.  Levels are reported beside it and are "
            f"calibrated by G3b below, because the caches move daily - idea 406.")
        for pn, d in g3.groupby("panel"):
            fr, ds = float(d["flip"].mean()), float(d["d_dSharpe"].max())
            ok_ = fr <= 0.01
            if ok_:
                repro.append(SMALL if pn == PARENT_SMALL else pn)
            log(f"     {pn:<9} n={len(d):5d}  win flips {int(d['flip'].sum()):4d} ({fr:.4f})  "
                f"max |dSharpe| {ds:.3e}  max |Sharpe| {float(d['d_Sharpe'].max()):.3e}  "
                f"max |g_eff| {float(d['d_g_eff'].max()):.3e}  -> {'PASS' if ok_ else 'FAIL'}")
        # G3b: the DATA-DRIFT calibrator.  SPY, RULES v1/v2 and the two ungated EWALL books carry
        # no gate and no twin, so any move in them is the caches moving under the record, not this
        # run's code.  It sets the scale a gated arm's drift must be read against.
        log(f"  G3b data-drift calibrator: five UNGATED reference books at rung {RUNG_HEAD:g} bps "
            f"vs idea 605's committed values (no gate, no twin -> pure cache drift):")
        pr = p605_refs
        cal = []
        for pn, rf in REFS.items():
            jn = PARENT_SMALL if pn == SMALL else pn
            for nm, key in (("SPY", "SPY"), ("v2", "v2"), ("v1", "v1"),
                            ("NOGATE g0.75", "NOGATE g0.75"), ("NOGATE g1.00", "NOGATE g1.00")):
                q = pr[(pr["panel"] == jn) & (pr["arm"] == key) & (pr["rung"] == RUNG_HEAD)]
                if not len(q) or key not in rf:
                    continue
                cal.append(dict(panel=pn, book=nm, Sharpe=rf[key][1],
                                Sharpe_605=float(q["Sharpe"].iloc[0]),
                                dS=abs(rf[key][1] - float(q["Sharpe"].iloc[0])),
                                dCAGR=abs(rf[key][0] - float(q["CAGR"].iloc[0]))))
        cal = pd.DataFrame(cal)
        log("     " + cal.to_string(index=False, float_format=lambda x: f"{x:.4f}")
            .replace("\n", "\n     "))
        for pn, d in cal.groupby("panel"):
            log(f"     {pn:<9} ungated drift: max |dSharpe| {d['dS'].max():.3e}, "
                f"max |dCAGR| {d['dCAGR'].max():.3e}")
        log(f"     G3 verdict: {len(repro)} of 3 panels reproduce -> {sorted(repro)}.")
        if SMALL not in repro:
            log("     The SMALL panel FAILS for the cache reason named above, not for a code "
                "reason: its g_eff differs, i.e. the breadth series is a different panel.")
    else:
        log("  G3 idea 605 cells.csv.gz NOT FOUND -> G3 cannot run")
    if PARENT_ORDER.exists():
        po = pd.read_csv(PARENT_ORDER).merge(full.reset_index(), on="rung", how="inner")
        log("     idea 605's published ordering.csv headline vs this run's three-panel rebuild "
            "(the SMALL swap moves it; both are printed, neither is edited):")
        log("     " + po[["rung", "win_ABS", "ABS", "win_QEXP", "QEXP", "win_QROLL", "QROLL"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n     "))

    log("\n" + "=" * 190)
    log(f"POPULATION: {len(grid)} grid points = {len(grid)//len(RUNGS)} twin pairs x {len(RUNGS)} "
        f"cost rungs ({grid['panel'].nunique()} panels x 18 arms x {len(DEPTHS)} depths x "
        f"{len(CADENCES)} cadences x {len(GROSSES)} gross).")
    log("Full-sample win rate by family and rung (this run's own rebuild of idea 605's headline):")
    log(full.to_string(float_format=lambda x: f"{x:.4f}"))

    # =================================================================== [1] the rolling census
    log("\n" + "=" * 190)
    log("[1] ROLLING CENSUS - the family ordering a reader standing in each window would have seen")

    rows, wrows = [], []
    for (W, ST), defs in sorted(win_defs.items()):
        # pooled across all panels, pooled across the two that reproduce idea 605, and per panel
        scopes = {"POOLED": list(WINS), "POOLED_REPRO": [p for p in WINS if p in repro]}
        scopes.update({p: [p] for p in WINS})
        for scope, only in scopes.items():
            if not only:
                continue
            for ri, c in enumerate(RUNGS):
                recs = []
                for k, (d0, d1) in enumerate(defs):
                    vals, ns = {}, {}
                    for f in FAMS:
                        wn = tt = 0
                        for p in only:
                            wn += int(WINS[p][(W, ST)][f][ri, k])
                            tt += int(TOTS[p][(W, ST)][f][ri, k])
                        vals[f] = wn / tt if tt else np.nan
                        ns[f] = tt
                    if min(ns.values()) == 0:
                        continue
                    o = order_of(vals)
                    recs.append(dict(W=W, step=ST, scope=scope, rung=c, k=k,
                                     start=d0.date(), end=d1.date(),
                                     win_ABS=vals["ABS"], win_QEXP=vals["QEXP"],
                                     win_QROLL=vals["QROLL"], n_ABS=ns["ABS"], n_QEXP=ns["QEXP"],
                                     n_QROLL=ns["QROLL"],
                                     order="".join(x[0] for x in o) if o else "TIE",
                                     order_full=" > ".join(o) if o else "TIE",
                                     match=bool(o == PUB_ORDER),
                                     top=o[0] if o else "TIE", bottom=o[-1] if o else "TIE",
                                     pair_RvE=vals["QROLL"] > vals["QEXP"],
                                     pair_EvA=vals["QEXP"] > vals["ABS"],
                                     pair_RvA=vals["QROLL"] > vals["ABS"],
                                     rho_vs_pub=spearman([vals[f] for f in FAMS],
                                                         [-PUB_ORDER.index(f) for f in FAMS])))
                if not recs:
                    continue
                d = pd.DataFrame(recs)
                wrows.append(d)
                rows.append(dict(W=W, step=ST, scope=scope, rung=c, n_win=len(d),
                                 match_rate=float(d["match"].mean()),
                                 top_QROLL=float((d["top"] == "QROLL").mean()),
                                 bottom_ABS=float((d["bottom"] == "ABS").mean()),
                                 pair_RvE=float(d["pair_RvE"].mean()),
                                 pair_EvA=float(d["pair_EvA"].mean()),
                                 pair_RvA=float(d["pair_RvA"].mean()),
                                 mean_rho=float(d["rho_vs_pub"].mean()),
                                 rho_eq1=float((d["rho_vs_pub"] > 0.999).mean()),
                                 n_tie=int((d["order"] == "TIE").sum()),
                                 mean_ABS=float(d["win_ABS"].mean()),
                                 mean_QEXP=float(d["win_QEXP"].mean()),
                                 mean_QROLL=float(d["win_QROLL"].mean())))
    census = pd.DataFrame(rows)
    windows = pd.concat(wrows, ignore_index=True)

    def cell(scope):
        return census[(census.W == W_HEAD) & (census["step"] == S_HEAD) &
                      (census.rung == RUNG_HEAD) & (census.scope == scope)].iloc[0]

    head = cell("POOLED")
    head_r = cell("POOLED_REPRO") if (census.scope == "POOLED_REPRO").any() else head
    log(f"\nHEADLINE CELL (declared before the run): window {W_HEAD}d, step {S_HEAD}d, "
        f"rung {RUNG_HEAD:g} bps, POOLED over all three panels, n = {int(head.n_win)} windows")
    log(f"  published order {' > '.join(PUB_ORDER)} seen in {head.match_rate:.4f} of windows "
        f"({int(round(head.match_rate*head.n_win))}/{int(head.n_win)})")
    log(f"  QROLL on top {head.top_QROLL:.4f} | ABS on bottom {head.bottom_ABS:.4f} | "
        f"pairwise QROLL>QEXP {head.pair_RvE:.4f}, QEXP>ABS {head.pair_EvA:.4f}, "
        f"QROLL>ABS {head.pair_RvA:.4f}")
    log(f"  mean rho vs published order {head.mean_rho:+.4f}; rho = +1 in {head.rho_eq1:.4f} of "
        f"windows; strict ties {int(head.n_tie)}")
    log(f"  mean family win rate over windows: ABS {head.mean_ABS:.4f}  QEXP {head.mean_QEXP:.4f}"
        f"  QROLL {head.mean_QROLL:.4f}")
    log(f"SAME CELL on the TWO PANELS THAT REPRODUCE idea 605 (POOLED_REPRO, the swapped small "
        f"panel dropped), n = {int(head_r.n_win)}:")
    log(f"  published order seen in {head_r.match_rate:.4f} | QROLL top {head_r.top_QROLL:.4f} | "
        f"ABS bottom {head_r.bottom_ABS:.4f} | mean rho {head_r.mean_rho:+.4f}")

    log(f"\nAGREEMENT RATE across BOTH tuned params, POOLED, rung {RUNG_HEAD:g} bps "
        f"(every grid point, none selected on):")
    piv = census[(census.scope == "POOLED") & (census.rung == RUNG_HEAD)].pivot(
        index="W", columns="step", values="match_rate")
    log(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    log("n windows behind each cell:")
    log(census[(census.scope == "POOLED") & (census.rung == RUNG_HEAD)].pivot(
        index="W", columns="step", values="n_win").to_string())

    log(f"\nAGREEMENT RATE across the COST ladder (POOLED, step {S_HEAD}d), every rung reported:")
    log(census[(census.scope == "POOLED") & (census["step"] == S_HEAD)].pivot(
        index="rung", columns="W", values="match_rate").to_string(
        float_format=lambda x: f"{x:.4f}"))

    log(f"\nPER-PANEL agreement at window {W_HEAD}d / step {S_HEAD}d, every rung:")
    log(census[(census.W == W_HEAD) & (census["step"] == S_HEAD)].pivot(
        index="rung", columns="scope", values="match_rate").to_string(
        float_format=lambda x: f"{x:.4f}"))

    log(f"\nPAIRWISE LEGS at window {W_HEAD}d / step {S_HEAD}d / rung {RUNG_HEAD:g}, per scope:")
    log(census[(census.W == W_HEAD) & (census["step"] == S_HEAD) & (census.rung == RUNG_HEAD)]
        [["scope", "n_win", "match_rate", "top_QROLL", "bottom_ABS", "pair_RvE", "pair_EvA",
          "pair_RvA", "mean_rho"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    log(f"\nWHICH ORDER a reader sees, window {W_HEAD}d / step {S_HEAD}d / rung {RUNG_HEAD:g}, "
        f"POOLED (R=QROLL, E=QEXP, A=ABS, top first):")
    hw = windows[(windows.W == W_HEAD) & (windows["step"] == S_HEAD) &
                 (windows.rung == RUNG_HEAD) & (windows.scope == "POOLED")]
    vc = hw["order_full"].value_counts()
    for o, n in vc.items():
        log(f"  {o:<28} {n:4d}  {n/len(hw):.4f}")

    # ---- Q4: within-window cost invariance
    piv0 = hw.set_index("k")[["win_ABS", "win_QEXP", "win_QROLL"]]
    hw100 = windows[(windows.W == W_HEAD) & (windows["step"] == S_HEAD) &
                    (windows.rung == 100.0) & (windows.scope == "POOLED")].set_index("k")
    hw0 = windows[(windows.W == W_HEAD) & (windows["step"] == S_HEAD) &
                  (windows.rung == 0.0) & (windows.scope == "POOLED")].set_index("k")
    common = hw0.index.intersection(hw100.index)
    same = float((hw0.loc[common, "order"].values == hw100.loc[common, "order"].values).mean())
    log(f"\nQ4 within-window cost invariance (window {W_HEAD}d/{S_HEAD}d, POOLED): the family order "
        f"at 0 bps equals the order at 100 bps in {same:.4f} of {len(common)} windows.")
    del piv0

    # =================================================================== [2] rule 8
    log("\n" + "=" * 190)
    log("[2] RULE 8 - the census as a SELECTOR: choose on IS (<= 2016) only, read once on OOS")

    # IS/OOS split of the master windows, then IS-only census -> family, then IS Sharpe -> arm
    defs = win_defs[(W_HEAD, S_HEAD)]
    is_end_ts, oos_ts = pd.Timestamp(IS_END), pd.Timestamp(OOS_START)
    is_k = [k for k, (d0, d1) in enumerate(defs) if d1 <= is_end_ts]
    oos_k = [k for k, (d0, d1) in enumerate(defs) if d0 >= oos_ts]
    hw_all = windows[(windows.W == W_HEAD) & (windows["step"] == S_HEAD) &
                     (windows.rung == RUNG_HEAD) & (windows.scope == "POOLED")]
    is_w = hw_all[hw_all["k"].isin(is_k)]
    oos_w = hw_all[hw_all["k"].isin(oos_k)]
    log(f"  IS windows (end <= {IS_END}): {len(is_w)};  OOS windows (start >= {OOS_START}): "
        f"{len(oos_w)};  straddling and therefore used by neither: "
        f"{len(hw_all) - len(is_w) - len(oos_w)}")
    is_top = is_w["top"].value_counts()
    oos_top = oos_w["top"].value_counts()
    log(f"  IS  top-family counts: {dict(is_top)}")
    log(f"  OOS top-family counts: {dict(oos_top)}")
    pick_fam = is_top.idxmax()
    oos_fam = oos_top.idxmax() if len(oos_top) else "n/a"
    log(f"  H7: IS pick = {pick_fam}; OOS most-often-top = {oos_fam} -> "
        f"{'PASS' if pick_fam == oos_fam else 'FAIL'}")
    log(f"  IS  match rate with the published order: {is_w['match'].mean():.4f}")
    log(f"  OOS match rate with the published order: {oos_w['match'].mean():.4f}")

    # the capital leg: one book, chosen on IS alone
    cand = grid[(grid.rung == RUNG_HEAD) & (grid.family == pick_fam)].copy()
    pick = cand.sort_values("IS_Sharpe", ascending=False).iloc[0]
    log(f"\n  RULE-8 BOOK (chosen on IS Sharpe alone, inside the IS-chosen family, read ONCE "
        f"on OOS): panel {pick.panel}, {pick.arm}, IS Sharpe {pick.IS_Sharpe:.3f}")
    ref = REFS[pick.panel]
    wf = []
    wf.append(dict(name=f"609 rule-8 pick: {pick.panel} {pick['arm']}", CAGR=pick.CAGR,
                   Sharpe=pick.Sharpe, MaxDD=pick.MaxDD, H1=pick.H1, H2=pick.H2,
                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD))
    for nm, key in (("RULES v2 baseline (live)", "v2"), ("RULES v1 (previous)", "v1"),
                    ("SPY", "SPY")):
        c_, s_, d_, h1_, h2_, oc_, os_, od_ = ref[key]
        wf.append(dict(name=f"{nm} [{pick.panel}]", CAGR=c_, Sharpe=s_, MaxDD=d_, H1=h1_, H2=h2_,
                       OOS_CAGR=oc_, OOS_Sharpe=os_, OOS_MaxDD=od_))
    # the matched-gross static twin of the pick, same rung
    tws = grid[(grid.rung == RUNG_HEAD) & (grid.panel == pick.panel) & (grid["arm"] == pick["arm"])]
    wfdf = pd.DataFrame(wf).set_index("name")
    log(wfdf.to_string(float_format=lambda x: f"{x:.4f}"))
    log(f"  the pick's MATCHED-GROSS STATIC TWIN at the same rung: Sharpe "
        f"{float(tws['twin_Sharpe'].iloc[0]):.4f}, dSharpe {float(tws['dSharpe'].iloc[0]):+.4f}, "
        f"dOOS {float(tws['dOOS'].iloc[0]):+.4f}")
    spy_r = ref["SPY"]
    p4b_oos = (pick.H1 > spy_r[3] and pick.H2 > spy_r[4] and pick.OOS_Sharpe > spy_r[6]
               and abs(pick.MaxDD) <= 0.60 * abs(spy_r[2]) and pick.CAGR >= 0.70 * spy_r[0])
    log(f"  H8: the rule-8 book passes 4b -> {'PASS' if p4b_oos else 'FAIL'} "
        f"(4a {'PASS' if pick.p4a else 'FAIL'}, 4b legs failing: {pick.fail4b})")

    # =================================================================== [3] both KEEP paths
    log("\n" + "=" * 190)
    log("[3] BOTH KEEP PATHS on EVERY grid point (PROTOCOL rule 4; nothing here is selected on)")
    log(f"  4a passes: {int(grid['p4a'].sum())} of {len(grid)}   "
        f"4b passes: {int(grid['p4b'].sum())} of {len(grid)}   "
        f"both: {int((grid['p4a'] & grid['p4b']).sum())}")
    log("  by panel x rung (4b):")
    log(grid.pivot_table(index="rung", columns="panel", values="p4b", aggfunc="sum")
        .to_string())
    log("  by panel x rung (4a):")
    log(grid.pivot_table(index="rung", columns="panel", values="p4a", aggfunc="sum")
        .to_string())
    log("  4b failing legs (whole grid): "
        + ", ".join(f"{k}:{v}" for k, v in grid["fail4b"].value_counts().items()))
    if grid["p4b"].any():
        log("  every 4b pass:")
        log(grid[grid["p4b"]][["panel", "rung", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                               "OOS_Sharpe", "dSharpe"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))

    # =================================================================== [4] hypotheses
    log("\n" + "=" * 190)
    log("[4] PRE-REGISTERED HYPOTHESES (bars declared in the docstring before the run)")
    ph = census[(census.scope == "POOLED") & (census.rung == RUNG_HEAD)]
    h4 = float(ph[ph["step"] == S_HEAD]["match_rate"].max() - ph[ph["step"] == S_HEAD]["match_rate"].min())
    h5 = float(ph[ph.W == W_HEAD]["match_rate"].max() - ph[ph.W == W_HEAD]["match_rate"].min())
    H = [
        ("H1 AGREEMENT   published order seen in >= 0.80 of headline windows",
         head.match_rate >= 0.80, f"{head.match_rate:.4f} (repro-panels {head_r.match_rate:.4f})"),
        ("H2 TOP         QROLL tops >= 0.90 of headline windows",
         head.top_QROLL >= 0.90, f"{head.top_QROLL:.4f} (repro-panels {head_r.top_QROLL:.4f})"),
        ("H3 BOTTOM      ABS is bottom in >= 0.80 of headline windows",
         head.bottom_ABS >= 0.80,
         f"{head.bottom_ABS:.4f} (repro-panels {head_r.bottom_ABS:.4f})"),
        ("H4 WINDOW-LEN  agreement moves < 0.15 across the 5 window lengths",
         h4 < 0.15, f"span {h4:.4f}"),
        ("H5 STEP        agreement moves < 0.05 across the 3 steps",
         h5 < 0.05, f"span {h5:.4f}"),
        ("H6 COST        order at 0 bps == order at 100 bps in >= 0.90 of windows",
         same >= 0.90, f"{same:.4f}"),
        ("H7 RULE-8 FAM  IS-top family == OOS-top family",
         pick_fam == oos_fam, f"IS {pick_fam} / OOS {oos_fam}"),
        ("H8 CAPITAL     the rule-8 book passes 4b",
         bool(p4b_oos), f"4a {pick.p4a} / 4b {pick.p4b} / fail {pick.fail4b}"),
    ]
    for t, ok_, v in H:
        log(f"  {'PASS' if ok_ else 'FAIL'}  {t:<66} {v}")
    log(f"  -> {sum(1 for _, o, _ in H if o)} of {len(H)} pre-registered hypotheses pass.")

    # =================================================================== outputs
    census.to_csv(OUT / f"{STEM}.census.csv", index=False)
    windows.to_csv(OUT / f"{STEM}.windows.csv.gz", index=False, compression="gzip")
    grid.to_csv(OUT / f"{STEM}.grid.csv.gz", index=False, compression="gzip")
    wfdf.to_csv(OUT / f"{STEM}.walkforward.csv")
    if len(g3):
        g3.to_csv(OUT / f"{STEM}.g3.csv.gz", index=False, compression="gzip")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    log(f"\nwrote {STEM}.census.csv / .windows.csv.gz / .grid.csv.gz / .walkforward.csv / "
        f".g3.csv.gz / .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()

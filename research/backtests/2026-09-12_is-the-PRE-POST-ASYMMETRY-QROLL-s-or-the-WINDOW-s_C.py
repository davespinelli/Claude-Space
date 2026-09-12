#!/usr/bin/env python3
"""Idea 834 - is the PRE/POST ASYMMETRY QROLL's or the WINDOW's?   (lane C, 2026-09-12)

QUESTION (QUEUE idea 834, verbatim)
    idea 825 measured adv_PRE -0.0602 against adv_POST +0.2315 at the record's split, but ABS's own
    win rate moved further (0.3333 -> 0.7407) than QROLL's (0.5231 -> 0.9722) in absolute terms.
    Score every family's PRE->POST delta against a family-blind control (the pooled arm set with
    family labels permuted 1,000 times) and report whether QROLL's delta is distinguishable from a
    relabelling.  Max 2 params (split date, permutation count).

WHAT IS BEING MEASURED, and the one thing the queue got wrong
    The object is idea 825's MATCHED-GROSS TWIN WIN RATE win[f] on a leg, and the new statistic is
    its PRE->POST movement
        delta[f] = win[f](POST) - win[f](PRE).
    The queue's premise is that ABS moved FURTHER than QROLL.  On 825's own published numbers that
    is arithmetically false: ABS 0.7407-0.3333 = +0.4074, QROLL 0.9722-0.5231 = +0.4491.  H_PREMISE
    below is pre-registered as the queue states it so the record carries the correction rather than
    the claim, and the substantive question - is QROLL's movement bigger than a relabelling of the
    same arms - is tested three ways because a raw delta on a BOUNDED rate is confounded by the
    level it starts from (QROLL starts at 0.5231 with 0.4769 of headroom and uses 94% of it; ABS
    starts at 0.3333 with 0.6667 and uses 61%).  The three statistics:
        RAW       delta[f]                                      (the queue's own reading)
        HEADROOM  delta[f] / (1 - win[f](PRE))                  ceiling-normalised
        LOGODDS   logit(win_POST) - logit(win_PRE), Haldane-corrected by 0.5/n on each leg
    All three at every grid point; none of them is a tuned parameter.

THE FAMILY-BLIND CONTROL (the queue's own specification)
    Pool every arm of the (panel, rung, matching, leg) cell, keep each arm's OWN (PRE, POST) win
    pair intact, and PERMUTE the family labels across arms, preserving the family sizes
    (3 ABS / 3 QEXP / 12 QROLL per panel per depth x cadence x gross cell -> 36/36/144 pooled).
    Each permutation yields a null delta[f] for every family.  Permuting LABELS and not outcomes is
    the right null: it destroys family identity while leaving the corpus, the window, the twin and
    the joint PRE/POST structure of every arm exactly as measured.  A two-sided permutation
    p-value is p = (1 + #{|null| >= |obs|}) / (1 + P).  Seeds are fixed (SEED0 + perm index), so
    the file is deterministic.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) SPLIT DATE in {2012-12-31, 2014-12-31, 2016-12-31, 2018-12-31, 2020-12-31}.  HEADLINE
        2016-12-31 = the record's IS/OOS boundary and 825's, declared here before any number.
    (2) PERMUTATION COUNT P in {200, 1000, 5000}.  HEADLINE 1000 = the count the queue names.
    5 x 3 = 15 grid points, every one printed and written to .grid.csv.

REPORTED AXES, none of them a tune (every one printed at every grid point):
    COST RUNG      {0, 10, 25} bps, headline 10 = PROTOCOL rule 2's.
    TWIN MATCHING  FULLMATCH (825's published construction: twin gross matched on the FULL sample,
                   path sliced to the leg) and WINMATCH (twin re-matched on the leg itself).  BOTH.
    PANEL          U56, B136, SMALL663 and POOLED over all three.
    STATISTIC      RAW, HEADROOM, LOGODDS as above.

PRE-REGISTERED HYPOTHESES (declared before any number is read)
    H_PREMISE   the queue's premise: |delta[ABS]| > |delta[QROLL]| (RAW) at the headline.
    H_QROLL     QROLL's RAW delta is distinguishable from a relabelling: p < 0.05 at the headline.
    H_ANYFAM    at least one family's RAW delta is distinguishable (p < 0.05) at the headline.
    H_ADV       the PRE->POST movement of adv = win[QROLL] - max(win[ABS], win[QEXP]) is
                distinguishable from a relabelling (p < 0.05) at the headline.
    H_CEILING   QROLL's verdict is the same under HEADROOM and LOGODDS as under RAW - i.e. it is
                not an artefact of how much room the family had left.
    H_SPLITFREE QROLL's RAW verdict (p < 0.05 or not) is the same at all 5 split dates.
    H_PERMSTAB  QROLL's RAW verdict is the same at P = 200, 1000, 5000.
    H_COSTINV   QROLL's RAW verdict is the same at 0, 10 and 25 bps.
    H_MATCH     QROLL's RAW verdict is the same under FULLMATCH and WINMATCH.
    H_PANEL     QROLL's RAW verdict agrees across U56, B136 and SMALL663 read separately.
    H_LEVEL     the PRE-leg LEVELS already order the families the way the deltas do - i.e. the
                movement is not just every family converging on the same POST ceiling.  Operational
                form: Spearman(win_PRE, delta_RAW) over the three families is NOT -1.
    H_R8CLAIM   RULE 8 ON THE CLAIM: the statistic (RAW/HEADROOM/LOGODDS) with the most significant
                QROLL p-value on the IS splits (<=2016-12-31) reproduces a p < 0.05 verdict on the
                LATER splits (>=2018-12-31), read ONCE.

GATES (printed first; no verdict is read until they are reported)
    G1 the vectorised runner reproduces products/backtester/engine.backtest to <= 1e-9.
    G2 the fast Sharpe/CAGR/MaxDD reproduce engine.metrics to <= 1e-9 on a real series.
    G3 the 0.01-grid interpolation of the static-gross twin reproduces an EXACT run to <= 1e-6.
    G4 this run's corpus reproduces idea 825's COMMITTED .arms.csv - Sharpe, twin Sharpe and the
       `win` boolean, all 1,944 rows.  834 is a re-reading of 825's numbers, so if the corpus does
       not rebuild, nothing downstream means anything.
    G5 825's published headline leg rates are reproduced (ABS 0.3333 / QEXP 0.5833 / QROLL 0.5231
       PRE, 0.7407 / 0.6481 / 0.9722 POST, adv -0.0602 / +0.2315).
    G6 the permutation null is CALIBRATED: the identity permutation returns delta exactly equal to
       the observed, and over 200 random family relabellings the share with p < 0.05 is within
       binomial tolerance of 0.05 (a null that rejects itself is not a null).

PROTOCOL RULE 8 (mandatory, run and reported) - on the BOOKS as well as on the claim:
    per (panel, family, gross, depth, cadence) the DIAL (level, w) is chosen on IS (..2016-12-31)
    by IS Sharpe alone and OOS (2017-01-01..) is read exactly ONCE, reported as CAGR/Sharpe/MaxDD
    against RULES v2 (the live baseline) and SPY on the same window.  BOTH KEEP paths (4a and 4b)
    are evaluated on all 648 arms at every cost rung, and each 4b passer is read against its own
    matched-gross twin so an exposure-only pass cannot be mistaken for a clause.

SURVIVORSHIP, up front: all three panels are CURRENT-constituent lists, so every LEVEL is
    optimistic and SMALL663 worst - a sub-$2B screen read today cannot see the names that fell out
    of it (data/SMALL_PANEL_README.md).  Tickers with max_1d_move >= 1.0 in data/small_meta.csv are
    dropped before anything is computed.  A win RATE is a within-panel agreement rate, which
    survivorship moves far less than a level, but no Sharpe or CAGR printed here is a capital claim.

Outputs (all committed under research/backtests/):
    .console.txt     full log
    .grid.csv        15 tuned points x 3 rungs x 2 matchings x 4 scopes x 3 statistics, every
                     cell: obs delta, null mean/sd, null 95% interval and the permutation p
    .balanced.csv    the POST-HOC arm-count-matched reading (QROLL cut to one w at a time)
    .arms.csv        one row per (panel, arm, rung): metrics, twin, legs, 4a/4b, rule-8 columns
    .walkforward.csv the rule-8 picks and their OOS reads against RULES v2 and SPY
    .result.md       the answer
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py are NOT
modified by this script.
"""
from __future__ import annotations

import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

DATE = "2026-09-12"
SLUG = "is-the-PRE-POST-ASYMMETRY-QROLL-s-or-the-WINDOW-s"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_C"
REF825 = HERE / "2026-09-12_is-QROLL-ON-TOP-an-entirely-POST-2017-fact_cloud.arms.csv"

# ---- 825's corpus constants, copied verbatim so G4 is a real reproduction --------------
FREQ = "W"
LAG = 1
MAX_VOL = 0.60
WARMUP = 260
GROSSES = [0.75, 1.00]
QS = [0.07, 0.12, 0.17]
BS = [0.30, 0.40, 0.50]
WS_ROLL = [252, 504, 1008, 2016]
DEPTHS = [0.25, 0.50, 1.00]
CADENCES = ["D", "W"]
MINQ = 252
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
TIE = 1e-12
SMALL_MAXMOVE = 1.0
FAMS = ["ABS", "QEXP", "QROLL"]
GSTEP = 0.01
MINLEG = 252
MATCHINGS = ["FULLMATCH", "WINMATCH"]
SCOPES = ["POOLED", "U56", "B136", "SMALL663"]
STATS = ["RAW", "HEADROOM", "LOGODDS"]

# ---- tuned dial 1 and 2, headlines declared here, before any number is read ------------
SPLITS = ["2012-12-31", "2014-12-31", "2016-12-31", "2018-12-31", "2020-12-31"]
SPLIT_HEAD = "2016-12-31"
SPLITS_IS = ["2012-12-31", "2014-12-31", "2016-12-31"]
SPLITS_OOS = ["2018-12-31", "2020-12-31"]
PERMS = [200, 1000, 5000]
PERM_HEAD = 1000
SEED0 = 8340000
ALPHA = 0.05

# 825's published headline, for G5 (hard-coded from its committed .result.md)
PUB = dict(PRE=dict(ABS=0.3333, QEXP=0.5833, QROLL=0.5231, adv=-0.0602),
           POST=dict(ABS=0.7407, QEXP=0.6481, QROLL=0.9722, adv=+0.2315))

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ runner (825's, verbatim)
def fast_run(prices, weights, mask, lag=LAG):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mk = mask.shift(lag, fill_value=False).values.copy()
    mk[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx))


def fmet(r):
    n = len(r)
    if n < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.rank().corr(b.rank()))


# ------------------------------------------------------------------ primitives (825's)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross, elig):
    e = elig.astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def _cadence(m, idx):
    return m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)


def gate_series(br, thr, depth, cadence, idx):
    below = (br < thr)
    m = pd.Series(1.0, index=idx).where(~below, 1.0 - depth)
    ok = br.notna() & (thr.notna() if isinstance(thr, pd.Series) else True)
    m = m.where(ok, 1.0)
    return _cadence(m, idx) if cadence == "W" else m


def panel(name):
    if name == "U56":
        px = load_universe()
    elif name == "B136":
        px = load_universe(broad=True)
    else:
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= SMALL_MAXMOVE, "ticker"])
        drop = [c for c in px.columns if c in bad and c != "SPY"]
        px = px.drop(columns=drop)
        P(f"   SMALL panel: dropped {len(drop)} tickers with max_1d_move >= {SMALL_MAXMOVE} "
          f"(data/small_meta.csv), {len([c for c in px.columns if c != 'SPY'])} left")
    return px.dropna(how="all").ffill()


class CS:
    """Cumulative sums of a stack of series, so any window's Sharpe is O(1)."""

    def __init__(self, M):
        z = np.zeros((M.shape[0], 1))
        self.s1 = np.concatenate([z, np.cumsum(M, axis=1)], axis=1)
        self.s2 = np.concatenate([z, np.cumsum(M * M, axis=1)], axis=1)

    def sharpe(self, a, b):
        n = b - a
        if n < 2:
            return np.full(self.s1.shape[0], np.nan)
        s1 = self.s1[:, b] - self.s1[:, a]
        s2 = self.s2[:, b] - self.s2[:, a]
        mu = s1 / n
        var = (s2 - n * mu * mu) / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)


class GridCS:
    """Cumsums of the static-gross twin grid incl. adjacent cross-products."""

    def __init__(self, N):
        self.G, self.T = N.shape
        z = np.zeros((self.G, 1))
        self.s1 = np.concatenate([z, np.cumsum(N, axis=1)], axis=1)
        self.s2 = np.concatenate([z, np.cumsum(N * N, axis=1)], axis=1)
        X = N[:-1] * N[1:]
        self.sx = np.concatenate([np.zeros((self.G - 1, 1)), np.cumsum(X, axis=1)], axis=1)

    def sharpe(self, a, b, lo, lam):
        n = b - a
        if n < 2:
            return np.full(len(lo), np.nan)
        hi = np.minimum(lo + 1, self.G - 1)
        m_lo = (self.s1[lo, b] - self.s1[lo, a]) / n
        m_hi = (self.s1[hi, b] - self.s1[hi, a]) / n
        q_lo = (self.s2[lo, b] - self.s2[lo, a]) / n
        q_hi = (self.s2[hi, b] - self.s2[hi, a]) / n
        xi = np.minimum(lo, self.G - 2)
        q_x = (self.sx[xi, b] - self.sx[xi, a]) / n
        mu = (1 - lam) * m_lo + lam * m_hi
        ey2 = (1 - lam) ** 2 * q_lo + 2 * lam * (1 - lam) * q_x + lam ** 2 * q_hi
        var = (ey2 - mu * mu) * n / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)


# ------------------------------------------------------------------ the three statistics
def _logit(p, n):
    """Haldane-corrected logit: (k + 0.5) / (n + 1) in odds form."""
    p = np.clip((p * n + 0.5) / (n + 1.0), 1e-12, 1 - 1e-12)
    return np.log(p / (1.0 - p))


def stat_delta(kind, pre, post, n_pre, n_post):
    """PRE->POST movement of a bounded rate, one of three readings.  Array-safe."""
    if kind == "RAW":
        return post - pre
    if kind == "HEADROOM":
        room = 1.0 - np.asarray(pre, float)
        with np.errstate(divide="ignore", invalid="ignore"):
            out = np.where(room > 1e-12, (post - pre) / np.where(room > 1e-12, room, 1.0), np.nan)
        return out if out.ndim else float(out)
    if kind == "LOGODDS":
        return _logit(post, n_post) - _logit(pre, n_pre)
    raise ValueError(kind)


def main():
    T0 = time.time()
    P(f"# Idea 834 - {SLUG}   (lane C, {DATE})")
    P("# QUESTION: score every family's PRE->POST delta in the matched-gross twin win rate against")
    P("#   a FAMILY-BLIND control (the pooled arm set with family labels permuted) and report")
    P("#   whether QROLL's delta is distinguishable from a relabelling.")
    P(f"# TUNED: split {SPLITS} x perms {PERMS} = {len(SPLITS)*len(PERMS)} points, ALL reported;")
    P(f"#   HEADLINE split {SPLIT_HEAD} (825's and the record's), P = {PERM_HEAD} (the queue's).")
    P(f"# REPORTED AXES (not tunes): rung {RUNGS} bps (headline {RUNG_HEAD:g}), matching {MATCHINGS},")
    P(f"#   scope {SCOPES}, statistic {STATS}.")
    P("# NULL: each arm keeps its own (PRE, POST) pair; FAMILY LABELS are permuted across arms with")
    P("#   family sizes preserved.  Two-sided p = (1 + #{|null| >= |obs|}) / (1 + P).  Seeds fixed.")
    P("# NOTE ON THE QUEUE'S PREMISE: on 825's own published numbers ABS moved +0.4074 and QROLL")
    P("#   +0.4491, so 'ABS moved further' is arithmetically false.  H_PREMISE tests it as stated.")
    P("# SURVIVORSHIP: all panels are current-constituent lists; levels optimistic, SMALL worst.")

    armrows, wfrows = [], []
    PAN = {}

    for pname in ["U56", "B136", "SMALL663"]:
        P(f"\n{'='*118}\nPANEL {pname}\n{'='*118}")
        px = panel(pname)
        idx = px.index
        start = idx[WARMUP]
        eidx = px.loc[start:].index
        T = len(eidx)
        mask = rebalance_mask(idx, FREQ)
        elig = eligible_mask(px)
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:].values
        P(f"   {px.shape[1]-1} tradeable names, {T} scored days {eidx[0].date()}..{eidx[-1].date()}")

        br_full = breadth(px)
        thr_exp = {q: br_full.expanding(min_periods=MINQ).quantile(q) for q in QS}
        thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q)
                    for q in QS for w in WS_ROLL}

        base0 = {}
        for g in GROSSES:
            rg, tn = fast_run(px, ewall_weights(px, g, elig), mask)
            base0[g] = (rg.loc[start:].values, tn.loc[start:].values)
        gg = np.round(np.arange(0.0, 1.0 + GSTEP / 2, GSTEP), 6)
        GR = np.zeros((len(gg), T))
        GT = np.zeros((len(gg), T))
        for i, x in enumerate(gg):
            if x == 0.0:
                continue
            rg, tn = fast_run(px, ewall_weights(px, float(x), elig), mask)
            GR[i], GT[i] = rg.loc[start:].values, tn.loc[start:].values

        if pname == "U56":
            P(f"\n{'-'*118}\nGATES G1-G3\n{'-'*118}")
            Wb = ewall_weights(px, 0.75, elig)
            rg, tn = fast_run(px, Wb, mask)
            eng = backtest(px, Wb, cost_bps=10, freq=FREQ)
            g1 = float(np.abs(((rg - tn * 10 / 1e4) - eng["returns"]).loc[start:].values).max())
            P(f"   G1 fast_run == engine.backtest                    max|d| {g1:.3e} "
              f"{'PASS' if g1 < 1e-9 else 'FAIL'}")
            assert g1 < 1e-9
            ser = pd.Series((rg - tn * 10 / 1e4).loc[start:].values)
            m = metrics(ser)
            fc, fs, fd = fmet(ser.values)
            g2 = max(abs(fc - m["CAGR"]), abs(fs - m["Sharpe"]), abs(fd - m["MaxDD"]))
            P(f"   G2 fast metrics == engine.metrics                 max|d| {g2:.3e} "
              f"{'PASS' if g2 < 1e-9 else 'FAIL'}")
            assert g2 < 1e-9
            xt = 0.6237
            lo = int(np.floor(round(xt, 6) / GSTEP))
            lam = (xt - gg[lo]) / GSTEP
            ex_r, ex_t = fast_run(px, ewall_weights(px, xt, elig), mask)
            en = (ex_r - ex_t * 10 / 1e4).loc[start:].values
            inn = ((1 - lam) * (GR[lo] - GT[lo] * 10 / 1e4)
                   + lam * (GR[lo + 1] - GT[lo + 1] * 10 / 1e4))
            g3 = abs(fsharpe(en) - fsharpe(inn))
            P(f"   G3 0.01-grid interpolation vs an EXACT twin run   |dSharpe| {g3:.3e} "
              f"{'PASS' if g3 < 1e-6 else 'FAIL'}  (g = {xt}, Sharpe {fsharpe(en):.6f})")
            assert g3 < 1e-6

        arms = ([("ABS", B, 0) for B in BS] + [("QEXP", q, 0) for q in QS]
                + [("QROLL", q, w) for q in QS for w in WS_ROLL])
        keys, ARM, TWF, GEFF_F, MEAN_ME = [], {c: [] for c in RUNGS}, {c: [] for c in RUNGS}, [], []
        for (fam, lev, w), d, cad in product(arms, DEPTHS, CADENCES):
            thr = lev if fam == "ABS" else (thr_exp[lev] if fam == "QEXP" else thr_roll[(lev, w)])
            m = gate_series(br_full, thr, d, cad, idx)
            me = m.reindex(eidx).shift(1).fillna(1.0).values
            sw = np.abs(np.diff(me, prepend=me[0]))
            for g in GROSSES:
                r0, t0 = base0[g]
                keys.append((fam, lev, w, d, cad, g))
                MEAN_ME.append(me)
                gf = g * float(me.mean())
                GEFF_F.append(gf)
                lo = int(np.floor(round(gf, 6) / GSTEP))
                lam = (gf - gg[lo]) / GSTEP
                for c in RUNGS:
                    ARM[c].append(me * r0 - (me * t0 + g * sw) * c / 1e4)
                    nlo = GR[lo] - GT[lo] * c / 1e4
                    hi = min(lo + 1, len(gg) - 1)
                    nhi = GR[hi] - GT[hi] * c / 1e4
                    TWF[c].append((1 - lam) * nlo + lam * nhi)
        K = len(keys)
        fam_of = np.array([k[0] for k in keys])
        w_of = np.array([k[2] for k in keys])
        gross_of = np.array([k[5] for k in keys])
        MEAN_ME = np.asarray(MEAN_ME)
        cs_me = np.concatenate([np.zeros((K, 1)), np.cumsum(MEAN_ME, axis=1)], axis=1)
        P(f"   {K} arms built ({int((fam_of=='ABS').sum())} ABS, {int((fam_of=='QEXP').sum())} "
          f"QEXP, {int((fam_of=='QROLL').sum())} QROLL); twin grid {len(gg)-1} runs")

        csA = {c: CS(np.asarray(ARM[c])) for c in RUNGS}
        csF = {c: CS(np.asarray(TWF[c])) for c in RUNGS}
        csG = {c: GridCS(GR - GT * c / 1e4) for c in RUNGS}

        # ---- full-sample arm table, rule 8 and both KEEP paths ----------------------
        h = T // 2
        is_end = int(eidx.searchsorted(pd.Timestamp(IS_END), side="right"))
        oos0 = int(eidx.searchsorted(pd.Timestamp(OOS_START), side="left"))
        sc, ss, sd_ = fmet(spy)
        spy_pack = (fsharpe(spy[:h]), fsharpe(spy[h:]), fsharpe(spy[oos0:]), sd_, sc)
        v2rg, v2tn = fast_run(px, rules_v2_weights(px), mask)
        v2rg, v2tn = v2rg.loc[start:].values, v2tn.loc[start:].values
        v1rg, v1tn = fast_run(px, rules_v1_weights(px), mask)
        v1rg, v1tn = v1rg.loc[start:].values, v1tn.loc[start:].values
        P(f"   SPY {sc:.2%} / {ss:.3f} / {sd_:.2%};  4b bars: CAGR floor {0.70*sc:.2%}, "
          f"DD cap {-0.60*abs(sd_):.2%}, halves {spy_pack[0]:.3f}/{spy_pack[1]:.3f}, "
          f"OOS {spy_pack[2]:.3f}")
        for c in RUNGS:
            v2 = v2rg - v2tn * c / 1e4
            b1, b2, bdd = fsharpe(v2[:h]), fsharpe(v2[h:]), fmet(v2)[2]
            A, F = np.asarray(ARM[c]), np.asarray(TWF[c])
            for i in range(K):
                fam, lev, w, d, cad, g = keys[i]
                ra, rt = A[i], F[i]
                ca, sa, da = fmet(ra)
                ct, st, dt = fmet(rt)
                oc, os_, od = fmet(ra[oos0:])
                t4b = dict(H1=fsharpe(ra[:h]) > spy_pack[0], H2=fsharpe(ra[h:]) > spy_pack[1],
                           OOS=os_ > spy_pack[2], DD=abs(da) <= 0.60 * abs(sd_),
                           CAGR=ca >= 0.70 * sc)
                armrows.append(dict(
                    panel=pname, rung=c, family=fam, level=lev, w=w, depth=d, cadence=cad, gross=g,
                    arm=f"{fam} L{lev} w{w} d{d:.2f} {cad} g{g:.2f}", g_eff=GEFF_F[i],
                    CAGR=ca, Sharpe=sa, MaxDD=da, H1=fsharpe(ra[:h]), H2=fsharpe(ra[h:]),
                    IS_Sharpe=fsharpe(ra[:is_end]), OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                    twin_CAGR=ct, twin_Sharpe=st, twin_MaxDD=dt, twin_OOS=fmet(rt[oos0:])[1],
                    dSharpe=sa - st, dOOS=os_ - fmet(rt[oos0:])[1],
                    win=bool(sa - st > TIE), tie=bool(abs(sa - st) <= TIE),
                    pass_4a=bool(fsharpe(ra[:h]) > b1 and fsharpe(ra[h:]) > b2 and da >= bdd),
                    pass_4b=all(t4b.values()),
                    fail_4b="+".join(k for k, v in t4b.items() if not v) or "-none-",
                    twin_pass_4b=bool(fsharpe(rt[:h]) > spy_pack[0]
                                      and fsharpe(rt[h:]) > spy_pack[1]
                                      and fmet(rt[oos0:])[1] > spy_pack[2]
                                      and abs(dt) <= 0.60 * abs(sd_) and ct >= 0.70 * sc),
                    SPY_CAGR=sc, SPY_Sharpe=ss, SPY_MaxDD=sd_, SPY_OOS_Sharpe=spy_pack[2],
                    SPY_OOS_CAGR=fmet(spy[oos0:])[0], SPY_OOS_MaxDD=fmet(spy[oos0:])[2],
                    V2_Sharpe=fsharpe(v2), V2_OOS_Sharpe=fsharpe(v2[oos0:]),
                    V2_OOS_CAGR=fmet(v2[oos0:])[0], V2_OOS_MaxDD=fmet(v2[oos0:])[2],
                    V1_Sharpe=fsharpe(v1rg - v1tn * c / 1e4)))
        ARdf = pd.DataFrame([a for a in armrows if a["panel"] == pname])
        for c in RUNGS:
            sub_c = ARdf[ARdf.rung == c]
            for fam in FAMS:
                for g in GROSSES:
                    for d in DEPTHS:
                        for cad in CADENCES:
                            s = sub_c[(sub_c.family == fam) & (sub_c.gross == g)
                                      & (sub_c.depth == d) & (sub_c.cadence == cad)]
                            if s.empty or s.IS_Sharpe.isna().all():
                                continue
                            pk = s.loc[s.IS_Sharpe.idxmax()]
                            wfrows.append(dict(panel=pname, rung=c, family=fam, gross=g, depth=d,
                                               cadence=cad, level=pk.level, w=pk.w,
                                               IS_Sharpe=pk.IS_Sharpe, OOS_CAGR=pk.OOS_CAGR,
                                               OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                                               OOS_dSharpe=pk.dOOS, pass_4a=bool(pk.pass_4a),
                                               pass_4b=bool(pk.pass_4b), fail_4b=pk.fail_4b,
                                               SPY_OOS_CAGR=pk.SPY_OOS_CAGR,
                                               SPY_OOS_Sharpe=pk.SPY_OOS_Sharpe,
                                               SPY_OOS_MaxDD=pk.SPY_OOS_MaxDD,
                                               V2_OOS_CAGR=pk.V2_OOS_CAGR,
                                               V2_OOS_Sharpe=pk.V2_OOS_Sharpe,
                                               V2_OOS_MaxDD=pk.V2_OOS_MaxDD))

        PAN[pname] = dict(eidx=eidx, csA=csA, csF=csF, csG=csG, fam=fam_of, w=w_of,
                          gross=gross_of, cs_me=cs_me, K=K, T=T, gg=gg)
        del px, GR, GT, ARM, TWF

    AR = pd.DataFrame(armrows)
    AR.to_csv(f"{OUT}.arms.csv", index=False)
    WF = pd.DataFrame(wfrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------------- G4: reproduce 825's corpus
    P(f"\n{'='*118}\nGATE G4 - does this run rebuild idea 825's COMMITTED corpus?\n{'='*118}")
    if REF825.exists():
        R = pd.read_csv(REF825)
        kcols = ["panel", "rung", "family", "level", "w", "depth", "cadence", "gross"]
        a = AR.set_index(kcols).sort_index()
        b = R.set_index(kcols).sort_index()
        same_idx = a.index.equals(b.index)
        d_sh = float(np.abs(a.Sharpe.values - b.Sharpe.values).max())
        d_tw = float(np.abs(a.twin_Sharpe.values - b.twin_Sharpe.values).max())
        d_win = int((a.win.values.astype(bool) != b.win.values.astype(bool)).sum())
        ok4 = same_idx and d_sh < 1e-12 and d_tw < 1e-12 and d_win == 0
        P(f"   rows {len(a)} vs {len(b)}, key sets identical {same_idx}")
        P(f"   max|dSharpe| {d_sh:.3e}   max|d twin Sharpe| {d_tw:.3e}   win-flag mismatches "
          f"{d_win}   {'PASS' if ok4 else 'FAIL'}")
    else:
        ok4 = False
        P(f"   FAIL - reference {REF825.name} not found")
    P(f"   G4 corpus reproduction: {'PASS' if ok4 else 'FAIL'}")

    # ------------------------------------------------------- leg machinery (825's, verbatim)
    def leg_rates(pname, c, a, b, matching):
        """win rate and arm count per family on [a,b) - plus the per-arm boolean vector."""
        d = PAN[pname]
        sa = d["csA"][c].sharpe(a, b)
        if matching == "FULLMATCH":
            st = d["csF"][c].sharpe(a, b)
        else:
            n = b - a
            gm = (d["cs_me"][:, b] - d["cs_me"][:, a]) / n * d["gross"]
            lo = np.floor(np.round(gm, 6) / GSTEP).astype(int)
            lo = np.clip(lo, 0, len(d["gg"]) - 2)
            lam = (gm - d["gg"][lo]) / GSTEP
            st = d["csG"][c].sharpe(a, b, lo, lam)
        ok = np.isfinite(sa) & np.isfinite(st)
        return (sa - st > TIE), ok

    def valid_panels(splitdate):
        """Panels whose BOTH legs are at least MINLEG days - so PRE and POST stack identically."""
        out = []
        for pname, d in PAN.items():
            cut = int(d["eidx"].searchsorted(pd.Timestamp(splitdate), side="right"))
            if cut >= MINLEG and d["T"] - cut >= MINLEG:
                out.append(pname)
        return out

    def leg_bools(c, splitdate, legname, matching, panels=None):
        """Per-arm win booleans for every panel on one leg, stacked with family labels."""
        pl = valid_panels(splitdate) if panels is None else panels
        wins, oks, fams, pans, wws = [], [], [], [], []
        for pname in pl:
            d = PAN[pname]
            cut = int(d["eidx"].searchsorted(pd.Timestamp(splitdate), side="right"))
            a, b = (0, cut) if legname == "PRE" else (cut, d["T"])
            wv, ok = leg_rates(pname, c, a, b, matching)
            wins.append(wv)
            oks.append(ok)
            fams.append(d["fam"])
            pans.append(np.full(d["K"], pname))
            wws.append(d["w"])
        if not wins:
            return None
        return (np.concatenate(wins), np.concatenate(oks), np.concatenate(fams),
                np.concatenate(pans), np.concatenate(wws))

    # ------------------------------------------------------- G5: 825's published headline
    P(f"\n{'='*118}\nGATE G5 - are idea 825's PUBLISHED headline leg rates reproduced?\n{'='*118}")
    g5bad = 0.0
    for legname in ["PRE", "POST"]:
        pk = leg_bools(RUNG_HEAD, SPLIT_HEAD, legname, "FULLMATCH")
        wv, ok, fv, _, _ = pk
        r = {f: float(wv[ok & (fv == f)].mean()) for f in FAMS}
        adv = r["QROLL"] - max(r["ABS"], r["QEXP"])
        diffs = {f: abs(r[f] - PUB[legname][f]) for f in FAMS}
        diffs["adv"] = abs(adv - PUB[legname]["adv"])
        g5bad = max([g5bad] + list(diffs.values()))
        P(f"   {legname:<5} " + "  ".join(f"{f} {r[f]:.4f} (pub {PUB[legname][f]:.4f})"
                                          for f in FAMS)
          + f"   adv {adv:+.4f} (pub {PUB[legname]['adv']:+.4f})")
    ok5 = g5bad <= 5e-4          # 825 published 4 decimals; half a unit in the last place
    P(f"   G5 max|this run - 825's published| {g5bad:.2e}  {'PASS' if ok5 else 'FAIL'} "
      f"(tolerance 5e-4, 825 published 4 dp)")

    # ------------------------------------------------------- G6: is the null calibrated?
    P(f"\n{'='*118}\nGATE G6 - is the family-blind null CALIBRATED?\n{'='*118}")
    pk_pre = leg_bools(RUNG_HEAD, SPLIT_HEAD, "PRE", "FULLMATCH")
    pk_post = leg_bools(RUNG_HEAD, SPLIT_HEAD, "POST", "FULLMATCH")
    wv0, ok0, fv0, _, wq0 = pk_pre
    wv1, ok1, _, _, _ = pk_post
    okb = ok0 & ok1
    P(f"   paired arms (finite on BOTH legs) {int(okb.sum())} of {len(okb)}; "
      + ", ".join(f"{f} {int((okb & (fv0 == f)).sum())}" for f in FAMS))

    def perm_pvals(wv_pre, wv_post, ok, fam, nperm, seed, labels=None):
        """Permutation test of delta[f] for all three statistics + the adv delta.

        The null permutes FAMILY LABELS across arms, preserving family sizes, while each arm
        keeps its own (PRE, POST) pair.  Vectorised: one (nperm x n) label matrix, family means
        by matrix product, so the whole null is three matmuls per leg.
        """
        lab = fam if labels is None else labels
        pre_v = wv_pre[ok].astype(float)
        post_v = wv_post[ok].astype(float)
        lab_v = lab[ok]
        n = len(pre_v)
        sizes = {f: int((lab_v == f).sum()) for f in FAMS}
        if min(sizes.values()) == 0:
            return {}
        obsP = {f: float(pre_v[lab_v == f].mean()) for f in FAMS}
        obsQ = {f: float(post_v[lab_v == f].mean()) for f in FAMS}

        def pack(Pm, Qm):
            """(stat, family) -> delta, for scalars or equal-length arrays."""
            d = {}
            for kind in STATS:
                for f in FAMS:
                    d[(kind, f)] = stat_delta(kind, Pm[f], Qm[f], sizes[f], sizes[f])
            d[("RAW", "ADV")] = ((Qm["QROLL"] - np.maximum(Qm["ABS"], Qm["QEXP"]))
                                 - (Pm["QROLL"] - np.maximum(Pm["ABS"], Pm["QEXP"])))
            return d

        obs = pack(obsP, obsQ)
        obs_adv_pre = obsP["QROLL"] - max(obsP["ABS"], obsP["QEXP"])
        obs_adv_post = obsQ["QROLL"] - max(obsQ["ABS"], obsQ["QEXP"])

        idxf = {f: i for i, f in enumerate(FAMS)}
        code = np.fromiter((idxf[x] for x in lab_v), dtype=np.int8, count=n)
        rng = np.random.default_rng(seed)
        PM = rng.permuted(np.tile(code, (nperm, 1)), axis=1)        # (nperm, n)
        nP, nQ = {}, {}
        for f in FAMS:
            M = (PM == idxf[f])
            nP[f] = (M * pre_v).sum(axis=1) / sizes[f]
            nQ[f] = (M * post_v).sum(axis=1) / sizes[f]
        nulls = pack(nP, nQ)

        out = {}
        for k, o in obs.items():
            nu = np.asarray(nulls[k], float)
            fin = nu[np.isfinite(nu)]
            pre_l = obs_adv_pre if k[1] == "ADV" else obsP[k[1]]
            post_l = obs_adv_post if k[1] == "ADV" else obsQ[k[1]]
            if not np.isfinite(o) or len(fin) == 0:
                out[k] = dict(obs=o, null_mean=np.nan, null_sd=np.nan, p=np.nan,
                              lo=np.nan, hi=np.nan, n=n, pre=pre_l, post=post_l)
                continue
            p = (1 + int((np.abs(fin) >= abs(o) - 1e-12).sum())) / (1 + len(fin))
            out[k] = dict(obs=float(o), null_mean=float(fin.mean()),
                          null_sd=float(fin.std(ddof=1)), p=float(p),
                          lo=float(np.quantile(fin, 0.025)), hi=float(np.quantile(fin, 0.975)),
                          n=n, pre=pre_l, post=post_l)
        return out

    # (a) the machinery must reproduce the directly-computed observed delta exactly
    chk = perm_pvals(wv0, wv1, okb, fv0, 50, SEED0 + 1)
    direct = {f: float(wv1[okb & (fv0 == f)].mean()) - float(wv0[okb & (fv0 == f)].mean())
              for f in FAMS}
    ident_max = max(abs(chk[("RAW", f)]["obs"] - direct[f]) for f in FAMS)
    ident = ident_max == 0.0
    P(f"   observed delta from the permutation machinery == direct leg difference: "
      f"max|d| {ident_max:.3e}  {'PASS' if ident else 'FAIL'}")

    # (b) calibration: 200 deliberately random relabellings, each tested against its own null
    nrej = 0
    ncal = 200
    rngc = np.random.default_rng(SEED0 + 999)
    base_codes = fv0[okb].copy()
    for t in range(ncal):
        lab = fv0.copy()
        lab[okb] = rngc.permutation(base_codes)
        res = perm_pvals(wv0, wv1, okb, fv0, 200, SEED0 + 5000 + t, labels=lab)
        if res[("RAW", "QROLL")]["p"] < ALPHA:
            nrej += 1
    share = nrej / ncal
    band = 1.96 * np.sqrt(ALPHA * (1 - ALPHA) / ncal)
    ok6 = ident and abs(share - ALPHA) <= band + 1.0 / 201
    P(f"   {ncal} random family relabellings, each scored against its own 200-permutation null:")
    P(f"   share with p < {ALPHA} = {share:.4f}  (expected {ALPHA}, binomial 95% band "
      f"+/-{band:.4f} plus the 1/(P+1) grid of {1/201:.4f})   {'PASS' if ok6 else 'FAIL'}")
    P(f"   G6 null calibration: {'PASS' if ok6 else 'FAIL'}")

    GATES = dict(G4=ok4, G5=ok5, G6=ok6)

    # ------------------------------------------------------- the grid
    P(f"\n{'='*118}")
    P(f"THE GRID - every one of the {len(SPLITS)*len(PERMS)} tuned points, at every reported axis.")
    P("delta = win(POST) - win(PRE) read three ways; p is the two-sided family-label permutation")
    P("p-value.  * marks p < 0.05.  'ADV' is the movement of win[QROLL] - max(win[ABS], win[QEXP]).")
    P(f"{'='*118}")

    gridrows, permrows = [], []   # permrows kept for readability; .grid.csv is the file
    CACHE = {}
    CELLSEED = [0]          # deterministic: a counter, never Python's randomised hash()

    def legpair(c, splitdate, matching):
        key = (c, splitdate, matching)
        if key not in CACHE:
            pl = valid_panels(splitdate)
            CACHE[key] = (leg_bools(c, splitdate, "PRE", matching, pl),
                          leg_bools(c, splitdate, "POST", matching, pl))
        return CACHE[key]

    hdr = (f"   {'split':<11}{'P':>6}{'rung':>5} {'match':<10}{'scope':<9}{'stat':<9}"
           f"{'family':<7}{'n':>5}{'winPRE':>8}{'winPOST':>9}{'delta':>9}"
           f"{'null mu':>9}{'null sd':>9}{'p':>8}")
    for splitdate in SPLITS:
        for nperm in PERMS:
            head_pt = (splitdate == SPLIT_HEAD and nperm == PERM_HEAD)
            P(f"\n   -- split {splitdate}  P {nperm}"
              + ("   <== HEADLINE" if head_pt else ""))
            P(hdr)
            for c in RUNGS:
                for matching in MATCHINGS:
                    A, B = legpair(c, splitdate, matching)
                    if A is None or B is None:
                        continue
                    wvA, okA, fvA, pnA, _ = A
                    wvB, okB, _, _, _ = B
                    for scope in SCOPES:
                        sel = okA & okB & ((pnA == scope) if scope != "POOLED" else True)
                        if sel.sum() < len(FAMS) * 3:
                            continue
                        CELLSEED[0] += 1
                        res = perm_pvals(wvA, wvB, sel, fvA, nperm, SEED0 + 10 * CELLSEED[0])
                        for (kind, f), r in res.items():
                            row = dict(split=splitdate, nperm=nperm, rung=c, matching=matching,
                                       scope=scope, stat=kind, family=f, n=r["n"],
                                       win_PRE=r.get("pre", np.nan), win_POST=r.get("post", np.nan),
                                       delta=r["obs"], null_mean=r["null_mean"],
                                       null_sd=r["null_sd"], null_lo=r["lo"], null_hi=r["hi"],
                                       p=r["p"], sig=bool(np.isfinite(r["p"])
                                                          and r["p"] < ALPHA),
                                       headline=head_pt)
                            gridrows.append(row)
                            permrows.append(row)
                            if head_pt and scope == "POOLED":
                                star = "*" if row["sig"] else " "
                                P(f"   {splitdate:<11}{nperm:>6}{c:>5.0f} {matching:<10}"
                                  f"{scope:<9}{kind:<9}{f:<7}{r['n']:>5}"
                                  f"{row['win_PRE']:>8.4f}{row['win_POST']:>9.4f}"
                                  f"{r['obs']:>9.4f}{r['null_mean']:>9.4f}{r['null_sd']:>9.4f}"
                                  f"{r['p']:>8.4f}{star}")
                            elif scope == "POOLED" and c == RUNG_HEAD \
                                    and matching == "FULLMATCH" and kind == "RAW":
                                star = "*" if row["sig"] else " "
                                P(f"   {splitdate:<11}{nperm:>6}{c:>5.0f} {matching:<10}"
                                  f"{scope:<9}{kind:<9}{f:<7}{r['n']:>5}"
                                  f"{row['win_PRE']:>8.4f}{row['win_POST']:>9.4f}"
                                  f"{r['obs']:>9.4f}{r['null_mean']:>9.4f}{r['null_sd']:>9.4f}"
                                  f"{r['p']:>8.4f}{star}")
    GD = pd.DataFrame(gridrows)
    GD.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"\n   {len(GD)} grid cells written to .grid.csv")

    # ------------------------------------------------------- hypotheses
    P(f"\n{'='*118}\nPRE-REGISTERED HYPOTHESES\n{'='*118}")

    def cell(family, stat="RAW", split=SPLIT_HEAD, nperm=PERM_HEAD, rung=RUNG_HEAD,
             match="FULLMATCH", scope="POOLED"):
        q = GD[(GD.split == split) & (GD.nperm == nperm) & (GD.rung == rung)
               & (GD.matching == match) & (GD.scope == scope) & (GD.stat == stat)
               & (GD.family == family)]
        return q.iloc[0] if len(q) else None

    H = {}
    cA, cQ, cR = cell("ABS"), cell("QEXP"), cell("QROLL")
    H["H_PREMISE"] = (abs(cA.delta) > abs(cR.delta),
                      f"|delta[ABS]| {abs(cA.delta):.4f} vs |delta[QROLL]| {abs(cR.delta):.4f}  "
                      f"(ABS {cA.win_PRE:.4f}->{cA.win_POST:.4f}, "
                      f"QROLL {cR.win_PRE:.4f}->{cR.win_POST:.4f})")
    H["H_QROLL"] = (cR.p < ALPHA,
                    f"QROLL RAW delta {cR.delta:+.4f}, null {cR.null_mean:+.4f} +/- "
                    f"{cR.null_sd:.4f}, 95% [{cR.null_lo:+.4f}, {cR.null_hi:+.4f}], p {cR.p:.4f}")
    sigs = {f: cell(f).p < ALPHA for f in FAMS}
    H["H_ANYFAM"] = (any(sigs.values()),
                     "p by family " + ", ".join(f"{f} {cell(f).p:.4f}" for f in FAMS))
    cAD = cell("ADV")
    H["H_ADV"] = (cAD is not None and cAD.p < ALPHA,
                  f"delta[adv] {cAD.delta:+.4f}, null {cAD.null_mean:+.4f} +/- {cAD.null_sd:.4f}, "
                  f"95% [{cAD.null_lo:+.4f}, {cAD.null_hi:+.4f}], p {cAD.p:.4f}")
    cH, cL = cell("QROLL", stat="HEADROOM"), cell("QROLL", stat="LOGODDS")
    same_ceil = ((cH.p < ALPHA) == (cR.p < ALPHA)) and ((cL.p < ALPHA) == (cR.p < ALPHA))
    H["H_CEILING"] = (same_ceil,
                      f"QROLL p RAW {cR.p:.4f} (d {cR.delta:+.4f}) / HEADROOM {cH.p:.4f} "
                      f"(d {cH.delta:+.4f}) / LOGODDS {cL.p:.4f} (d {cL.delta:+.4f})")
    sv = {s: cell("QROLL", split=s) for s in SPLITS}
    H["H_SPLITFREE"] = (len({(v.p < ALPHA) for v in sv.values() if v is not None}) == 1,
                        "QROLL p by split " + ", ".join(
                            f"{s[:4]} {v.p:.4f} (d {v.delta:+.4f})"
                            for s, v in sv.items() if v is not None))
    pvv = {n: cell("QROLL", nperm=n) for n in PERMS}
    H["H_PERMSTAB"] = (len({(v.p < ALPHA) for v in pvv.values() if v is not None}) == 1,
                       "QROLL p by P " + ", ".join(f"P{n} {v.p:.4f}"
                                                   for n, v in pvv.items() if v is not None))
    cvv = {c: cell("QROLL", rung=c) for c in RUNGS}
    H["H_COSTINV"] = (len({(v.p < ALPHA) for v in cvv.values() if v is not None}) == 1,
                      "QROLL p by rung " + ", ".join(f"{c:g}bps {v.p:.4f} (d {v.delta:+.4f})"
                                                     for c, v in cvv.items() if v is not None))
    mvv = {m: cell("QROLL", match=m) for m in MATCHINGS}
    H["H_MATCH"] = (len({(v.p < ALPHA) for v in mvv.values() if v is not None}) == 1,
                    "QROLL p by matching " + ", ".join(f"{m} {v.p:.4f} (d {v.delta:+.4f})"
                                                       for m, v in mvv.items() if v is not None))
    vvv = {s: cell("QROLL", scope=s) for s in ["U56", "B136", "SMALL663"]}
    H["H_PANEL"] = (len({(v.p < ALPHA) for v in vvv.values() if v is not None}) == 1,
                    "QROLL p by panel " + ", ".join(f"{s} {v.p:.4f} (d {v.delta:+.4f})"
                                                    for s, v in vvv.items() if v is not None))
    pre_levels = [cell(f).win_PRE for f in FAMS]
    raw_deltas = [cell(f).delta for f in FAMS]
    rho_lvl = spearman(pre_levels, raw_deltas)
    H["H_LEVEL"] = (not (np.isfinite(rho_lvl) and rho_lvl <= -0.999),
                    f"Spearman(win_PRE, delta_RAW) over the 3 families {rho_lvl:+.4f}  "
                    + ", ".join(f"{f} {cell(f).win_PRE:.4f}->{cell(f).delta:+.4f}" for f in FAMS))
    # rule 8 ON THE CLAIM
    is_p = {k: float(np.mean([cell("QROLL", stat=k, split=s).p for s in SPLITS_IS
                              if cell("QROLL", stat=k, split=s) is not None])) for k in STATS}
    pick = min(STATS, key=lambda k: is_p[k])
    oos_p = [cell("QROLL", stat=pick, split=s) for s in SPLITS_OOS]
    oos_ok = all(v is not None and v.p < ALPHA for v in oos_p)
    H["H_R8CLAIM"] = (oos_ok,
                      f"statistic chosen on IS splits {SPLITS_IS} by mean QROLL p = {pick} "
                      f"(mean p " + ", ".join(f"{k} {is_p[k]:.4f}" for k in STATS)
                      + "); read ONCE on " + ", ".join(
                          f"{s[:4]} p {v.p:.4f} (d {v.delta:+.4f})"
                          for s, v in zip(SPLITS_OOS, oos_p) if v is not None) + ")")
    for k, (ok, why) in H.items():
        P(f"   {k:<12} {'PASS' if ok else 'FAIL'}   {why}")

    # ------------------------------------------------------- the decomposition table
    A, B = legpair(RUNG_HEAD, SPLIT_HEAD, "FULLMATCH")
    wvA, okA, fvA, pnA, wqA = A
    wvB, okB, _, _, _ = B
    P(f"\n{'='*118}\nTHE DECOMPOSITION - every family, every statistic, at the headline\n{'='*118}")
    P(f"   {'stat':<9}{'family':<7}{'n':>5}{'winPRE':>8}{'winPOST':>9}{'delta':>9}{'null mu':>9}"
      f"{'null sd':>9}{'z':>7}{'null 95% lo':>12}{'hi':>9}{'p':>8}  verdict")
    NFAM = {f: int(((fvA == f) & okA & okB).sum()) for f in FAMS}
    NFAM["ADV"] = int((okA & okB).sum())
    for kind in STATS:
        for f in FAMS + (["ADV"] if kind == "RAW" else []):
            v = cell(f, stat=kind)
            if v is None:
                continue
            z = (v.delta - v.null_mean) / v.null_sd if v.null_sd else np.nan
            P(f"   {kind:<9}{f:<7}{NFAM[f]:>5}{v.win_PRE:>8.4f}{v.win_POST:>9.4f}{v.delta:>9.4f}"
              f"{v.null_mean:>9.4f}{v.null_sd:>9.4f}{z:>7.2f}{v.null_lo:>12.4f}{v.null_hi:>9.4f}"
              f"{v.p:>8.4f}  {'DISTINGUISHABLE' if v.p < ALPHA else 'indistinguishable'}")

    # --- POST-HOC MECHANISM (declared post-hoc; NOT a pre-registered hypothesis) ----------
    P(f"\n{'='*118}")
    P("POST-HOC MECHANISM - is 'DISTINGUISHABLE' a FAMILY fact or an ARM-COUNT fact?")
    P("Declared POST-HOC, after the table above was read, and flagged as such: the corpus gives")
    P("QROLL 432 of the 648 pooled arms against 108 each for ABS and QEXP, so a permuted QROLL")
    P("group is two thirds of the whole pool and its null is mechanically the TIGHTEST.  Below,")
    P("QROLL is cut to ONE lookback w at a time (36 arms/panel = 108 pooled, exactly ABS's and")
    P("QEXP's count) so all three families face an equally wide null.  All four w are reported.")
    P(f"{'='*118}")
    P(f"   {'corpus':<14}{'nQROLL':>7}  {'family':<7}{'delta':>9}{'null mu':>9}{'null sd':>9}"
      f"{'z':>8}{'p':>8}  verdict")
    balrows = []
    for wsel in ["ALL"] + WS_ROLL:
        keep = okA & okB
        if wsel != "ALL":
            keep = keep & ((fvA != "QROLL") | (wqA == wsel))
        nq = int((keep & (fvA == "QROLL")).sum())
        CELLSEED[0] += 1
        res = perm_pvals(wvA, wvB, keep, fvA, PERM_HEAD, SEED0 + 10 * CELLSEED[0])
        for f in FAMS + ["ADV"]:
            r = res.get(("RAW", f))
            if r is None:
                continue
            z = ((r["obs"] - r["null_mean"]) / r["null_sd"]
                 if r["null_sd"] and np.isfinite(r["null_sd"]) else np.nan)
            balrows.append(dict(corpus=f"QROLL w={wsel}", n_QROLL=nq, family=f, delta=r["obs"],
                                null_mean=r["null_mean"], null_sd=r["null_sd"], z=z, p=r["p"],
                                sig=bool(r["p"] < ALPHA)))
            P(f"   {'QROLL w='+str(wsel):<14}{nq:>7}  {f:<7}{r['obs']:>9.4f}{r['null_mean']:>9.4f}"
              f"{r['null_sd']:>9.4f}{z:>8.2f}{r['p']:>8.4f}  "
              f"{'DISTINGUISHABLE' if r['p'] < ALPHA else 'indistinguishable'}")
    BAL = pd.DataFrame(balrows)
    BAL.to_csv(f"{OUT}.balanced.csv", index=False)
    qbal = BAL[(BAL.family == "QROLL") & (BAL.corpus != "QROLL w=ALL")]
    abal = BAL[(BAL.family == "ADV") & (BAL.corpus != "QROLL w=ALL")]
    P(f"   ARM-COUNT-MATCHED READING: QROLL's delta is distinguishable in "
      f"{int(qbal.sig.sum())} of {len(qbal)} single-w corpora (null sd "
      f"{qbal.null_sd.min():.4f}-{qbal.null_sd.max():.4f} against {BAL[(BAL.family=='QROLL') & (BAL.corpus=='QROLL w=ALL')].null_sd.iloc[0]:.4f} "
      f"at w=ALL); the ADV movement in {int(abal.sig.sum())} of {len(abal)}.")

    P(f"\n   Sign/verdict stability of QROLL's RAW delta over ALL "
      f"{len(GD[(GD.stat=='RAW') & (GD.family=='QROLL')])} (split, P, rung, matching, scope) cells:")
    QR = GD[(GD.stat == "RAW") & (GD.family == "QROLL")]
    P(f"   delta > 0 in {int((QR.delta > 0).sum())}/{len(QR)}; p < {ALPHA} in "
      f"{int(QR.sig.sum())}/{len(QR)}; median p {QR.p.median():.4f}, min {QR.p.min():.4f}, "
      f"max {QR.p.max():.4f}")
    for f in FAMS + ["ADV"]:
        S = GD[(GD.stat == "RAW") & (GD.family == f)]
        P(f"     {f:<7} delta>0 {int((S.delta>0).sum()):>4}/{len(S):<4} "
          f"sig {int(S.sig.sum()):>4}/{len(S):<4} median delta {S.delta.median():+.4f} "
          f"median p {S.p.median():.4f}")

    # ------------------------------------------------------- rule 8 on the BOOKS
    P(f"\n{'='*118}\nPROTOCOL RULE 8 ON THE BOOKS, and BOTH KEEP PATHS\n{'='*118}")
    P(f"   dial (level, w) chosen on IS (..{IS_END}) by IS Sharpe; OOS ({OOS_START}..) read ONCE.")
    P(f"   {'panel':<9}{'rung':>5} {'family':<7}{'picks':>6}{'OOS CAGR':>10}{'OOS Sh':>8}"
      f"{'OOS DD':>9} | {'v2 CAGR':>9}{'v2 Sh':>7}{'v2 DD':>8} | {'SPY CAGR':>9}{'SPY Sh':>7}"
      f"{'SPY DD':>8} |{'4a':>4}{'4b':>4}")
    for pname in ["U56", "B136", "SMALL663"]:
        for c in RUNGS:
            for fam in FAMS:
                s = WF[(WF.panel == pname) & (WF.rung == c) & (WF.family == fam)]
                if s.empty:
                    continue
                P(f"   {pname:<9}{c:>5.0f} {fam:<7}{len(s):>6}{s.OOS_CAGR.mean():>10.2%}"
                  f"{s.OOS_Sharpe.mean():>8.3f}{s.OOS_MaxDD.mean():>9.2%} | "
                  f"{s.V2_OOS_CAGR.iloc[0]:>9.2%}{s.V2_OOS_Sharpe.iloc[0]:>7.3f}"
                  f"{s.V2_OOS_MaxDD.iloc[0]:>8.2%} | {s.SPY_OOS_CAGR.iloc[0]:>9.2%}"
                  f"{s.SPY_OOS_Sharpe.iloc[0]:>7.3f}{s.SPY_OOS_MaxDD.iloc[0]:>8.2%} |"
                  f"{int(s.pass_4a.sum()):>4}{int(s.pass_4b.sum()):>4}")
    P(f"\n   FULL-SAMPLE KEEP paths over all {len(AR)} (panel, arm, rung) rows:")
    for pname in ["U56", "B136", "SMALL663"]:
        for c in RUNGS:
            s = AR[(AR.panel == pname) & (AR.rung == c)]
            n4b = int(s.pass_4b.sum())
            twinpass = int(s[s.pass_4b].twin_pass_4b.sum()) if n4b else 0
            P(f"   {pname:<9}{c:>5.0f} bps   4a {int(s.pass_4a.sum()):>3}/{len(s):<4} "
              f"4b {n4b:>3}/{len(s):<4}  of the 4b passers, {twinpass} have a twin that ALSO "
              f"passes 4b (exposure, not clause)")
    P(f"   TOTAL full-sample: 4a {int(AR.pass_4a.sum())}/{len(AR)}, "
      f"4b {int(AR.pass_4b.sum())}/{len(AR)};  rule-8 picks: 4a {int(WF.pass_4a.sum())}/{len(WF)}, "
      f"4b {int(WF.pass_4b.sum())}/{len(WF)}")
    best = WF.loc[WF.OOS_Sharpe.idxmax()]
    P(f"   best rule-8 pick by OOS Sharpe: {best.panel} {best.family} L{best.level} w{best.w} "
      f"d{best.depth:.2f} {best.cadence} g{best.gross:.2f} @ {best.rung:g} bps -> OOS "
      f"{best.OOS_CAGR:.2%} / {best.OOS_Sharpe:.3f} / {best.OOS_MaxDD:.2%} "
      f"(4a {bool(best.pass_4a)}, 4b {bool(best.pass_4b)}, twin dSharpe {best.OOS_dSharpe:+.4f})")

    # ------------------------------------------------------- verdict
    P(f"\n{'='*118}\nVERDICT\n{'='*118}")
    P(f"   GATES: " + "  ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in GATES.items())
      + "  (G1-G3 above)")
    npass = sum(1 for ok, _ in H.values() if ok)
    P(f"   {npass} of {len(H)} pre-registered hypotheses PASS.")
    P(f"   Headline (split {SPLIT_HEAD}, P {PERM_HEAD}, {RUNG_HEAD:g} bps, FULLMATCH, POOLED, RAW):")
    for f in FAMS + ["ADV"]:
        v = cell(f)
        P(f"     {f:<7} {v.win_PRE:.4f} -> {v.win_POST:.4f}   delta {v.delta:+.4f}   "
          f"null 95% [{v.null_lo:+.4f}, {v.null_hi:+.4f}]   p {v.p:.4f}  "
          f"{'DISTINGUISHABLE from a relabelling' if v.p < ALPHA else 'INDISTINGUISHABLE'}")
    if cR.p < ALPHA:
        ans = ("QROLL's - the PRE->POST movement is LARGER for QROLL than a family-blind "
               "relabelling of the same arms produces")
    elif any(cell(f).p < ALPHA for f in FAMS):
        ans = ("THE WINDOW'S for QROLL, but not for every family - QROLL's own delta is "
               "indistinguishable from a relabelling while another family's is not")
    else:
        ans = ("THE WINDOW'S - no family's PRE->POST delta is distinguishable from a "
               "family-blind relabelling of the same arms")
    P(f"   ANSWER: the asymmetry is {ans}.")
    P(f"   KEEP claimed: none by construction - this run prices a PUBLISHED STATISTIC, not a book.")
    P("   The KEEP paths and rule-8 walk-forward above are reported for every arm as PROTOCOL")
    P("   requires; no arm is promoted by this script.")
    P(f"\n   runtime {time.time()-T0:.1f}s")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return H, GATES, GD, AR, WF, ans


if __name__ == "__main__":
    main()

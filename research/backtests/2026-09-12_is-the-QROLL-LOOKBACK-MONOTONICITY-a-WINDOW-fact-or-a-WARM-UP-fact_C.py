#!/usr/bin/env python3
"""Idea 843 - is the QROLL PRE/POST delta's LOOKBACK MONOTONICITY a WINDOW-LENGTH fact or a
WARM-UP fact?   (lane C, 2026-09-12)

QUESTION (QUEUE idea 843, verbatim)
    idea 834's arm-count-matched reading falls monotonically in the rolling-quantile lookback
    (+0.7222 at w252, +0.5000 at w504, +0.3889 at w1008, +0.1852 and insignificant at w2016), and
    w2016 is eight years of warm-up on a sample that starts in 2009, so its PRE leg is nearly empty
    at every split <=2016.  Separate the two channels by re-running each w on a leg that starts only
    once its own threshold exists.  Max 2 params (w, leg start rule).

THE TWO CHANNELS, stated before any number is read
    A QROLL arm's gate is `breadth < rolling(w, min_periods=w).quantile(q)`.  Until w observations
    exist the threshold is NaN and `gate_series` sets the multiplier to 1.0, so THE ARM IS THE
    UNGATED BOOK - not approximately, bit-identically (G6 proves this at run time).  On the record's
    2009-start panels the PRE leg of a w=2016 arm is therefore 87.4% dead on U56/B136 and 100% dead
    on SMALL663 at the record's 2016-12-31 split.
        WINDOW channel  a longer lookback makes a genuinely different, slower-moving threshold, so
                        the family's PRE->POST movement really is smaller.
        WARM-UP channel a longer lookback simply has less gate in the PRE leg, so its PRE win rate
                        is the ungated book's win rate and the movement is mechanically compressed.
    Idea 834's RAW reading cannot tell them apart because both are monotone in w.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) LOOKBACK w in {252, 504, 1008, 2016}, plus the w=ALL corpus for continuity with 834.
        Every w is reported; there is no headline w - the w-profile IS the object.
    (2) LEG START RULE in {RAW, LIVE, COMMON}.  HEADLINE LIVE = the queue's own instruction,
        declared here before any number.
            RAW     834's / 825's convention: the PRE leg starts at the first scored day.
            LIVE    the queue's: each arm's PRE leg starts on the first day ITS OWN threshold
                    exists (ABS and QEXP are live from day one, so only QROLL moves).
            COMMON  every arm in the corpus starts on the LONGEST w's live day, so the legs are
                    calendar-identical AND every threshold exists.  LIVE alone cannot settle the
                    question because it gives each w a different calendar; COMMON holds the
                    calendar fixed and is the leg on which a surviving w-profile is a WINDOW fact.
    5 w-corpora x 3 rules = 15 tuned points, every one printed and written to .grid.csv.

REPORTED AXES, none of them a tune (every one computed at every tuned point)
    SPLIT DATE     {2012,2014,2016,2018,2020}-12-31.  HEADLINE 2016-12-31 = the record's IS/OOS
                   boundary, 825's and 834's, declared here before any number.  It is an AXIS here,
                   not a dial: 834 already spent a parameter on it.
    COST RUNG      {0, 10, 25} bps, headline 10 = PROTOCOL rule 2's.
    TWIN MATCHING  FULLMATCH (825's: twin gross matched on the FULL sample, path sliced to the leg)
                   and WINMATCH (twin re-matched on the leg actually used).  BOTH.
    PANEL          U56, B136, SMALL663 and POOLED.
    STATISTIC      RAW, HEADROOM (delta / (1 - win_PRE)) and LOGODDS, 834's three readings.
    PERMUTATIONS   P = 1000 throughout, the count 834 used and the queue named.

THE CORPUS AND THE NULL are 834's, unchanged: 216 arms per panel (3 ABS / 3 QEXP / 12 QROLL levels
    x 3 depths x 2 cadences x 2 gross), win = does the arm beat its own matched-gross static twin on
    the leg, and the family-blind null permutes FAMILY LABELS across arms with family sizes
    preserved, each arm keeping its own (PRE, POST) pair.  Every reading here is ARM-COUNT-MATCHED
    (QROLL cut to one w, 108 arms pooled, exactly ABS's and QEXP's count) because that is the
    reading idea 843 quotes.  Two-sided p = (1 + #{|null| >= |obs|}) / (1 + P); seeds fixed.

PRE-REGISTERED HYPOTHESES (declared before any number is read)
    H_REPRO     under RAW at the headline split this run reproduces 834's committed per-w deltas
                (+0.7222 / +0.5000 / +0.3889 / +0.1852).
    H_MONO_RAW  under RAW the QROLL delta is strictly decreasing in w (Spearman = -1).
    H_WARMUP    WARM-UP channel: under LIVE the spread max(delta) - min(delta) over the four w
                shrinks by at least 50% against RAW at the headline split.
    H_WINDOW    WINDOW channel: under COMMON the profile is still strictly decreasing in w
                (Spearman = -1) at the most recent split where COMMON is feasible on all panels.
    H_LIVEFIT   the PRE leg's LIVE SHARE explains the RAW delta at least as well as log w does
                (|Spearman| and univariate R^2, over all feasible (w, split, panel) cells).
    H_W2016SIG  w=2016's QROLL delta, insignificant under RAW at the headline, becomes
                distinguishable (p < 0.05) once its leg is restricted to live days.
    H_COSTINV   the w-profile's monotonicity verdict is the same at 0, 10 and 25 bps.
    H_MATCH     the w-profile's monotonicity verdict is the same under FULLMATCH and WINMATCH.
    H_PANEL     the w-profile's monotonicity verdict agrees across U56, B136 and SMALL663.
    H_R8CLAIM   RULE 8 ON THE CLAIM: the leg rule chosen on the IS splits (<=2016-12-31) as the one
                with the flattest w-profile reproduces that verdict on the later splits (>=2018),
                read once.
    H_R8PICK    RULE 8 ON THE BOOKS: the (level, w) pick changes when the chooser is restricted to
                arms whose threshold is live over the IS window (834's chooser is warm-up-blind and
                can pick a w that did not exist for most of the window it was chosen on).

GATES (printed first; no verdict is read until they are reported)
    G1 the vectorised runner reproduces products/backtester/engine.backtest to <= 1e-9.
    G2 the fast Sharpe/CAGR/MaxDD reproduce engine.metrics to <= 1e-9 on a real series.
    G3 the 0.01-grid interpolation of the static-gross twin reproduces an EXACT run to <= 1e-6.
    G4 this run's corpus reproduces idea 834's COMMITTED .arms.csv - Sharpe, twin Sharpe and the
       `win` boolean, all 1,944 rows.  843 re-reads 834's numbers; if the corpus does not rebuild,
       nothing downstream means anything.
    G5 this run reproduces idea 834's COMMITTED .balanced.csv - the four per-w deltas the queue
       quotes, to 1e-12.
    G6 THE INERTNESS IDENTITY (this run's own): on every day before its threshold exists, a QROLL
       arm's gate multiplier is exactly 1.0 and its daily return is BIT-IDENTICAL to the ungated
       EWALL book at the same gross.  max|d| must be exactly 0.0.  This is what makes "warm-up" an
       arithmetic fact rather than a story.
    G7 the family-blind null is CALIBRATED: the identity permutation returns the observed delta,
       and over 200 random relabellings the p < 0.05 share is within binomial tolerance of 0.05.

PROTOCOL RULE 8 (mandatory, run and reported) - on the BOOKS as well as on the claim:
    per (panel, family, gross, depth, cadence) the DIAL (level, w) is chosen on IS (..2016-12-31)
    by IS Sharpe alone and OOS (2017-01-01..) is read exactly ONCE, reported as CAGR/Sharpe/MaxDD
    against RULES v2 (the live baseline) and SPY on the same window.  THREE choosers are reported:
        BLIND    834's - every arm is a candidate (a w that was dead for 87% of IS can be picked).
        LIVE50   candidates restricted to arms live for >= 50% of the IS window.
        LIVELEG  every arm is a candidate but its IS Sharpe is read on its OWN live segment of IS.
    BOTH KEEP paths (4a and 4b) are evaluated on all 648 arms at every cost rung.

SURVIVORSHIP, up front: all three panels are CURRENT-constituent lists, so every LEVEL is
    optimistic and SMALL663 worst - a sub-$2B screen read today cannot see the names that fell out
    of it (data/SMALL_PANEL_README.md).  Tickers with max_1d_move >= 1.0 in data/small_meta.csv are
    dropped before anything is computed.  A win RATE is a within-panel agreement rate, which
    survivorship moves far less than a level, but no Sharpe or CAGR printed here is a capital claim.

Outputs (all committed under research/backtests/):
    .console.txt     full log
    .grid.csv        every (w-corpus, rule, split, rung, matching, scope, statistic, family) cell
    .liveness.csv    per (panel, w, split, rule): leg bounds, length, live share, dead-day count
    .arms.csv        one row per (panel, arm, rung): metrics, twin, 4a/4b, rule-8 columns
    .walkforward.csv the three choosers' rule-8 picks and their OOS reads vs RULES v2 and SPY
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
SLUG = "is-the-QROLL-LOOKBACK-MONOTONICITY-a-WINDOW-fact-or-a-WARM-UP-fact"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_C"
REF834 = HERE / "2026-09-12_is-the-PRE-POST-ASYMMETRY-QROLL-s-or-the-WINDOW-s_C"

# ---- 834's / 825's corpus constants, copied verbatim so G4 is a real reproduction ------
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
PANELS = ["U56", "B136", "SMALL663"]

# ---- tuned dial 1 and 2, headlines declared here, before any number is read ------------
WSELS = ["ALL"] + WS_ROLL
RULES_LEG = ["RAW", "LIVE", "COMMON"]
RULE_HEAD = "LIVE"
SPLITS = ["2012-12-31", "2014-12-31", "2016-12-31", "2018-12-31", "2020-12-31"]
SPLIT_HEAD = "2016-12-31"
SPLITS_IS = ["2012-12-31", "2014-12-31", "2016-12-31"]
SPLITS_OOS = ["2018-12-31", "2020-12-31"]
NPERM = 1000
SEED0 = 8430000
ALPHA = 0.05
LIVE_BAR = 0.50            # the LIVE50 chooser's bar, reported not tuned

# 834's committed per-w RAW deltas, for G5 / H_REPRO (read from its .balanced.csv at run time,
# with these as the published fallback so the gate is real even if the file moves)
PUB834 = {252: 0.7222222222222222, 504: 0.49999999999999994,
          1008: 0.38888888888888884, 2016: 0.18518518518518512}

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ runner (825's/834's, verbatim)
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


def r2(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3 or x.std() == 0 or y.std() == 0:
        return np.nan
    return float(np.corrcoef(x, y)[0, 1] ** 2)


# ------------------------------------------------------------------ primitives (825's/834's)
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

    def sharpe_rows(self, a_arr, b, rows=None):
        """Per-arm start index (the LIVE / COMMON rules need this), one scalar end."""
        out = np.full(self.s1.shape[0], np.nan)
        sel = np.arange(self.s1.shape[0]) if rows is None else np.asarray(rows)
        for a in np.unique(np.asarray(a_arr)[sel]):
            who = sel[np.asarray(a_arr)[sel] == a]
            if b - int(a) < 2:
                continue
            out[who] = self.sharpe(int(a), b)[who]
        return out


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


# ------------------------------------------------------------------ the three statistics (834's)
def _logit(p, n):
    p = np.clip((p * n + 0.5) / (n + 1.0), 1e-12, 1 - 1e-12)
    return np.log(p / (1.0 - p))


def stat_delta(kind, pre, post, n_pre, n_post):
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


def perm_pvals(wv_pre, wv_post, ok, fam, nperm, seed, labels=None):
    """Family-blind permutation test (834's, verbatim): permute FAMILY LABELS across arms with
    family sizes preserved; each arm keeps its own (PRE, POST) pair."""
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
    PM = rng.permuted(np.tile(code, (nperm, 1)), axis=1)
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
            out[k] = dict(obs=o, null_mean=np.nan, null_sd=np.nan, p=np.nan, lo=np.nan, hi=np.nan,
                          n=n, pre=pre_l, post=post_l, nQ=sizes["QROLL"])
            continue
        p = (1 + int((np.abs(fin) >= abs(o) - 1e-12).sum())) / (1 + len(fin))
        out[k] = dict(obs=float(o), null_mean=float(fin.mean()), null_sd=float(fin.std(ddof=1)),
                      p=float(p), lo=float(np.quantile(fin, 0.025)),
                      hi=float(np.quantile(fin, 0.975)), n=n, pre=pre_l, post=post_l,
                      nQ=sizes["QROLL"])
    return out


def main():
    T0 = time.time()
    P(f"# Idea 843 - {SLUG}   (lane C, {DATE})")
    P("# QUESTION: is the w-monotonicity of QROLL's PRE->POST twin-win delta a WINDOW-LENGTH fact")
    P("#   or a WARM-UP fact?  Re-run each w on a leg that starts once its own threshold exists.")
    P(f"# TUNED: w {WSELS} x leg rule {RULES_LEG} = {len(WSELS)*len(RULES_LEG)} points, ALL")
    P(f"#   reported; HEADLINE rule {RULE_HEAD} (the queue's own instruction).  No headline w -")
    P("#   the w-profile is the object.")
    P(f"# REPORTED AXES (not tunes): split {SPLITS} (headline {SPLIT_HEAD}), rung {RUNGS} bps")
    P(f"#   (headline {RUNG_HEAD:g}), matching {MATCHINGS}, scope {SCOPES}, statistic {STATS},")
    P(f"#   permutations P = {NPERM} throughout (834's count).")
    P("# NULL: 834's family-blind control - family labels permuted across arms, sizes preserved,")
    P("#   each arm keeping its own (PRE, POST) pair.  Every reading is ARM-COUNT-MATCHED.")
    P("# SURVIVORSHIP: all panels are current-constituent lists; levels optimistic, SMALL worst.")

    armrows, wfrows, liverows = [], [], []
    PAN = {}

    for pname in PANELS:
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

        # ---- live index per family/w: the first scored day on which the gate can act ----
        def live_index(thr):
            if not isinstance(thr, pd.Series):
                return 0
            v = thr.reindex(eidx).shift(1).notna().values
            nz = np.flatnonzero(v)
            return int(nz[0]) if len(nz) else T

        LIVE_W = {w: live_index(thr_roll[(QS[0], w)]) for w in WS_ROLL}
        for w in WS_ROLL:
            assert all(live_index(thr_roll[(q, w)]) == LIVE_W[w] for q in QS), \
                "live index must not depend on the quantile level"
        LIVE_EXP = live_index(thr_exp[QS[0]])
        COMMON_IDX = max(LIVE_W.values())
        P(f"   live index (first day the gate can act): ABS 0, QEXP {LIVE_EXP}, "
          + ", ".join(f"w{w} {LIVE_W[w]} ({eidx[LIVE_W[w]].date() if LIVE_W[w] < T else 'never'})"
                      for w in WS_ROLL))
        P(f"   COMMON start index = {COMMON_IDX} "
          f"({eidx[COMMON_IDX].date() if COMMON_IDX < T else 'never'})")

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
        keys, ARM, TWF, GEFF_F, MEAN_ME, LIVEI = [], {c: [] for c in RUNGS}, \
            {c: [] for c in RUNGS}, [], [], []
        g6_max = 0.0
        g6_cells = 0
        for (fam, lev, w), d, cad in product(arms, DEPTHS, CADENCES):
            thr = lev if fam == "ABS" else (thr_exp[lev] if fam == "QEXP" else thr_roll[(lev, w)])
            m = gate_series(br_full, thr, d, cad, idx)
            me = m.reindex(eidx).shift(1).fillna(1.0).values
            sw = np.abs(np.diff(me, prepend=me[0]))
            li = 0 if fam == "ABS" else (LIVE_EXP if fam == "QEXP" else LIVE_W[w])
            for g in GROSSES:
                r0, t0 = base0[g]
                keys.append((fam, lev, w, d, cad, g))
                MEAN_ME.append(me)
                LIVEI.append(li)
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
                # ---- G6: the inertness identity, on this arm's own dead region ----
                if fam == "QROLL" and li > 0:
                    dead = slice(0, li)
                    ung = r0[dead] - t0[dead] * RUNG_HEAD / 1e4
                    got = ARM[RUNG_HEAD][-1][dead]
                    g6_max = max(g6_max, float(np.abs(got - ung).max()),
                                 float(np.abs(me[dead] - 1.0).max()))
                    g6_cells += 1
        K = len(keys)
        fam_of = np.array([k[0] for k in keys])
        w_of = np.array([k[2] for k in keys])
        gross_of = np.array([k[5] for k in keys])
        live_of = np.asarray(LIVEI, int)
        MEAN_ME = np.asarray(MEAN_ME)
        cs_me = np.concatenate([np.zeros((K, 1)), np.cumsum(MEAN_ME, axis=1)], axis=1)
        P(f"   {K} arms built ({int((fam_of=='ABS').sum())} ABS, {int((fam_of=='QEXP').sum())} "
          f"QEXP, {int((fam_of=='QROLL').sum())} QROLL); twin grid {len(gg)-1} runs")
        P(f"   G6 inertness identity on {g6_cells} QROLL arms: max|arm - ungated EWALL| on the "
          f"dead region = {g6_max:.3e}  {'PASS' if g6_max == 0.0 else 'FAIL'}")

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
                li = int(live_of[i])
                is_live_share = float(max(is_end - li, 0) / is_end) if is_end else np.nan
                is_live_sharpe = fsharpe(ra[li:is_end]) if is_end - li >= MINLEG else np.nan
                t4b = dict(H1=fsharpe(ra[:h]) > spy_pack[0], H2=fsharpe(ra[h:]) > spy_pack[1],
                           OOS=os_ > spy_pack[2], DD=abs(da) <= 0.60 * abs(sd_),
                           CAGR=ca >= 0.70 * sc)
                armrows.append(dict(
                    panel=pname, rung=c, family=fam, level=lev, w=w, depth=d, cadence=cad, gross=g,
                    arm=f"{fam} L{lev} w{w} d{d:.2f} {cad} g{g:.2f}", g_eff=GEFF_F[i],
                    live_idx=li, live_date=str(eidx[li].date()) if li < T else "never",
                    IS_live_share=is_live_share,
                    CAGR=ca, Sharpe=sa, MaxDD=da, H1=fsharpe(ra[:h]), H2=fsharpe(ra[h:]),
                    IS_Sharpe=fsharpe(ra[:is_end]), IS_live_Sharpe=is_live_sharpe,
                    OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
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

        # ---- rule 8 on the books: three choosers ------------------------------------
        for c in RUNGS:
            sub_c = ARdf[ARdf.rung == c]
            for fam in FAMS:
                for g in GROSSES:
                    for d in DEPTHS:
                        for cad in CADENCES:
                            s = sub_c[(sub_c.family == fam) & (sub_c.gross == g)
                                      & (sub_c.depth == d) & (sub_c.cadence == cad)]
                            if s.empty:
                                continue
                            for chooser in ["BLIND", "LIVE50", "LIVELEG"]:
                                if chooser == "BLIND":
                                    cand, col = s, "IS_Sharpe"
                                elif chooser == "LIVE50":
                                    cand, col = s[s.IS_live_share >= LIVE_BAR], "IS_Sharpe"
                                else:
                                    cand, col = s, "IS_live_Sharpe"
                                cand = cand[cand[col].notna()]
                                if cand.empty:
                                    wfrows.append(dict(panel=pname, rung=c, family=fam, gross=g,
                                                       depth=d, cadence=cad, chooser=chooser,
                                                       level=np.nan, w=np.nan,
                                                       no_candidate=True))
                                    continue
                                pk = cand.loc[cand[col].idxmax()]
                                wfrows.append(dict(
                                    panel=pname, rung=c, family=fam, gross=g, depth=d, cadence=cad,
                                    chooser=chooser, no_candidate=False, level=pk.level, w=pk.w,
                                    IS_live_share=pk.IS_live_share, IS_Sharpe=pk.IS_Sharpe,
                                    IS_live_Sharpe=pk.IS_live_Sharpe,
                                    OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                                    OOS_MaxDD=pk.OOS_MaxDD, OOS_dSharpe=pk.dOOS,
                                    pass_4a=bool(pk.pass_4a), pass_4b=bool(pk.pass_4b),
                                    fail_4b=pk.fail_4b,
                                    SPY_OOS_CAGR=pk.SPY_OOS_CAGR,
                                    SPY_OOS_Sharpe=pk.SPY_OOS_Sharpe,
                                    SPY_OOS_MaxDD=pk.SPY_OOS_MaxDD,
                                    V2_OOS_CAGR=pk.V2_OOS_CAGR, V2_OOS_Sharpe=pk.V2_OOS_Sharpe,
                                    V2_OOS_MaxDD=pk.V2_OOS_MaxDD))

        PAN[pname] = dict(eidx=eidx, csA=csA, csF=csF, csG=csG, fam=fam_of, w=w_of,
                          gross=gross_of, cs_me=cs_me, K=K, T=T, gg=gg, live=live_of,
                          live_w=LIVE_W, common=COMMON_IDX, g6=g6_max)
        del px, GR, GT, ARM, TWF

    AR = pd.DataFrame(armrows)
    AR.to_csv(f"{OUT}.arms.csv", index=False)
    WF = pd.DataFrame(wfrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    G6 = max(PAN[p]["g6"] for p in PANELS)

    # ------------------------------------------------------- G4: reproduce 834's corpus
    P(f"\n{'='*118}\nGATE G4 - does this run rebuild idea 834's COMMITTED corpus?\n{'='*118}")
    ref = Path(f"{REF834}.arms.csv")
    if ref.exists():
        R = pd.read_csv(ref)
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
        P(f"   FAIL - reference {ref.name} not found")
    P(f"   G4 corpus reproduction: {'PASS' if ok4 else 'FAIL'}")

    # ------------------------------------------------------- leg machinery
    def leg_start(pname, wsel, rule, fam_arr, w_arr, live_arr):
        """PRE-leg start index for a whole (panel, w-corpus, rule) cell.

        The start is applied to EVERY arm in the corpus, ABS and QEXP included, so the three
        families are always compared on the SAME leg and the family-blind null stays exact.
            RAW     0                 (834's / 825's convention)
            LIVE    live(w of this corpus)   - the queue's "starts once its own threshold exists"
            COMMON  live(longest w)          - LIVE plus a calendar held fixed across the w-profile
        For the w=ALL and w=2016 corpora LIVE and COMMON coincide by construction.
        """
        d = PAN[pname]
        n = len(fam_arr)
        if rule == "RAW":
            return np.zeros(n, int)
        if rule == "LIVE":
            w = max(WS_ROLL) if wsel == "ALL" else int(wsel)
            return np.full(n, d["live_w"][w], int)
        if rule == "COMMON":
            return np.full(n, d["common"], int)
        raise ValueError(rule)

    def leg_rates(pname, c, a_arr, b, matching, rows=None):
        """win boolean and finiteness per arm on [a_i, b) with per-arm starts."""
        d = PAN[pname]
        sa = d["csA"][c].sharpe_rows(a_arr, b, rows)
        if matching == "FULLMATCH":
            st = d["csF"][c].sharpe_rows(a_arr, b, rows)
        else:
            st = np.full(d["K"], np.nan)
            sel = np.arange(d["K"]) if rows is None else np.asarray(rows)
            for a in np.unique(np.asarray(a_arr)[sel]):
                who = sel[np.asarray(a_arr)[sel] == a]
                a = int(a)
                n = b - a
                if n < 2:
                    continue
                gm = (d["cs_me"][:, b] - d["cs_me"][:, a]) / n * d["gross"]
                lo = np.clip(np.floor(np.round(gm, 6) / GSTEP).astype(int), 0, len(d["gg"]) - 2)
                lam = (gm - d["gg"][lo]) / GSTEP
                st[who] = d["csG"][c].sharpe(a, b, lo, lam)[who]
        ok = np.isfinite(sa) & np.isfinite(st)
        return (sa - st > TIE), ok

    def corpus(c, splitdate, matching, wsel, rule):
        """Arm-count-matched PRE/POST win vectors pooled over the panels where the cell is
        feasible.  Returns None when no panel is feasible."""
        wins_pre, wins_post, oks, fams, pans = [], [], [], [], []
        feas = []
        for pname in PANELS:
            d = PAN[pname]
            cut = int(d["eidx"].searchsorted(pd.Timestamp(splitdate), side="right"))
            keep = np.ones(d["K"], bool)
            if wsel != "ALL":
                keep &= (d["fam"] != "QROLL") | (d["w"] == wsel)
            a_arr = leg_start(pname, wsel, rule, d["fam"], d["w"], d["live"])
            rows = np.flatnonzero(keep)
            # feasibility: EVERY kept arm needs >= MINLEG days on BOTH legs
            if len(rows) == 0:
                continue
            pre_len = cut - a_arr[rows]
            if pre_len.min() < MINLEG or d["T"] - cut < MINLEG:
                liverows.append(dict(panel=pname, wsel=str(wsel), rule=rule, split=splitdate,
                                     feasible=False, pre_start=int(a_arr[rows].max()),
                                     pre_len=int(pre_len.min()), post_len=int(d["T"] - cut),
                                     live_share=np.nan))
                continue
            feas.append(pname)
            wvA, okA = leg_rates(pname, c, a_arr, cut, matching, rows)
            wvB, okB = leg_rates(pname, c, np.zeros(d["K"], int) + cut, d["T"], matching, rows)
            wins_pre.append(wvA[rows])
            wins_post.append(wvB[rows])
            oks.append((okA & okB)[rows])
            fams.append(d["fam"][rows])
            pans.append(np.full(len(rows), pname))
            if c == RUNG_HEAD and matching == "FULLMATCH":
                qw = wsel if wsel != "ALL" else max(WS_ROLL)
                lw = d["live_w"].get(qw, 0)
                liverows.append(dict(panel=pname, wsel=str(wsel), rule=rule, split=splitdate,
                                     feasible=True, pre_start=int(a_arr[rows].max()),
                                     pre_len=int(pre_len.min()), post_len=int(d["T"] - cut),
                                     live_share=float(max(cut - lw, 0) / cut) if cut else np.nan))
        if not wins_pre:
            return None
        return (np.concatenate(wins_pre), np.concatenate(wins_post), np.concatenate(oks),
                np.concatenate(fams), np.concatenate(pans), feas)

    # ------------------------------------------------------- G5: reproduce 834's per-w deltas
    P(f"\n{'='*118}\nGATE G5 - does this run reproduce idea 834's COMMITTED per-w deltas?\n{'='*118}")
    balref = Path(f"{REF834}.balanced.csv")
    pub = dict(PUB834)
    if balref.exists():
        B = pd.read_csv(balref)
        B = B[(B.family == "QROLL") & (B.corpus != "QROLL w=ALL")]
        pub = {int(str(r.corpus).split("=")[1]): float(r.delta) for r in B.itertuples()}
        P(f"   read {len(pub)} committed deltas from {balref.name}")
    else:
        P("   committed .balanced.csv not found - using the deltas published in 834's result.md")
    g5 = 0.0
    got5 = {}
    for w in WS_ROLL:
        pk = corpus(RUNG_HEAD, SPLIT_HEAD, "FULLMATCH", w, "RAW")
        if pk is None:
            P(f"   w={w}: no feasible panel under RAW - cannot check")
            g5 = np.inf
            continue
        wvA, wvB, ok, fv, _, feas = pk
        dlt = (float(wvB[ok & (fv == "QROLL")].mean())
               - float(wvA[ok & (fv == "QROLL")].mean()))
        got5[w] = dlt
        g5 = max(g5, abs(dlt - pub[w]))
        P(f"   w={w:<5} this run {dlt:+.10f}   834 committed {pub[w]:+.10f}   "
          f"|d| {abs(dlt-pub[w]):.2e}   panels {','.join(feas)}")
    ok5 = g5 < 1e-12
    P(f"   G5 max|this run - 834| {g5:.3e}  {'PASS' if ok5 else 'FAIL'}  (H_REPRO)")
    P(f"\n   G6 inertness identity (all panels): max|d| {G6:.3e}  "
      f"{'PASS' if G6 == 0.0 else 'FAIL'}")
    P("      => before its threshold exists a QROLL arm IS the ungated EWALL book, bit-identically.")

    # ------------------------------------------------------- G7: null calibration
    P(f"\n{'='*118}\nGATE G7 - is the family-blind null CALIBRATED?\n{'='*118}")
    pk = corpus(RUNG_HEAD, SPLIT_HEAD, "FULLMATCH", 252, "RAW")
    wv0, wv1, okb, fv0, _, _ = pk
    chk = perm_pvals(wv0, wv1, okb, fv0, 50, SEED0 + 1)
    direct = {f: float(wv1[okb & (fv0 == f)].mean()) - float(wv0[okb & (fv0 == f)].mean())
              for f in FAMS}
    ident_max = max(abs(chk[("RAW", f)]["obs"] - direct[f]) for f in FAMS)
    ident = ident_max == 0.0
    P(f"   observed delta from the permutation machinery == direct leg difference: "
      f"max|d| {ident_max:.3e}  {'PASS' if ident else 'FAIL'}")
    nrej, ncal = 0, 200
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
    ok7 = ident and abs(share - ALPHA) <= band + 1.0 / 201
    P(f"   {ncal} random family relabellings vs their own 200-permutation null: share p < {ALPHA} "
      f"= {share:.4f} (expected {ALPHA}, band +/-{band:.4f} + grid {1/201:.4f})  "
      f"{'PASS' if ok7 else 'FAIL'}")
    GATES = dict(G4=ok4, G5=ok5, G6=(G6 == 0.0), G7=ok7)

    # ------------------------------------------------------- the grid
    P(f"\n{'='*118}")
    P(f"THE GRID - all {len(WSELS)*len(RULES_LEG)} tuned points at every reported axis.")
    P("delta = win(POST) - win(PRE); p is the two-sided family-label permutation p-value; * = sig.")
    P("An INFEASIBLE cell is one where some arm's PRE leg is shorter than "
      f"{MINLEG} days under that rule.")
    P(f"{'='*118}")
    gridrows = []
    CELLSEED = [0]
    hdr = (f"   {'rule':<8}{'w':<7}{'split':<12}{'rung':>5} {'match':<10}{'scope':<9}{'stat':<9}"
           f"{'family':<7}{'n':>5}{'winPRE':>8}{'winPOST':>9}{'delta':>9}{'null mu':>9}"
           f"{'null sd':>9}{'p':>8}")
    for rule in RULES_LEG:
        for wsel in WSELS:
            for splitdate in SPLITS:
                for c in RUNGS:
                    for matching in MATCHINGS:
                        pk = corpus(c, splitdate, matching, wsel, rule)
                        if pk is None:
                            if c == RUNG_HEAD and matching == "FULLMATCH":
                                gridrows.append(dict(rule=rule, wsel=str(wsel), split=splitdate,
                                                     rung=c, matching=matching, scope="POOLED",
                                                     stat="RAW", family="QROLL", feasible=False))
                            continue
                        wvA, wvB, okp, fv, pn, feas = pk
                        for scope in SCOPES:
                            sel = okp & ((pn == scope) if scope != "POOLED" else True)
                            if sel.sum() < len(FAMS) * 3:
                                continue
                            CELLSEED[0] += 1
                            res = perm_pvals(wvA, wvB, sel, fv, NPERM, SEED0 + 10 * CELLSEED[0])
                            for (kind, f), r in res.items():
                                gridrows.append(dict(
                                    rule=rule, wsel=str(wsel), split=splitdate, rung=c,
                                    matching=matching, scope=scope, stat=kind, family=f,
                                    feasible=True, panels=",".join(feas), n=r["n"],
                                    n_QROLL=r["nQ"], win_PRE=r["pre"], win_POST=r["post"],
                                    delta=r["obs"], null_mean=r["null_mean"],
                                    null_sd=r["null_sd"], null_lo=r["lo"], null_hi=r["hi"],
                                    p=r["p"],
                                    sig=bool(np.isfinite(r["p"]) and r["p"] < ALPHA),
                                    headline=(rule == RULE_HEAD and splitdate == SPLIT_HEAD
                                              and c == RUNG_HEAD and matching == "FULLMATCH"
                                              and scope == "POOLED")))
        P(f"   ... rule {rule} done ({time.time()-T0:.0f}s)")
    GD = pd.DataFrame(gridrows)
    GD.to_csv(f"{OUT}.grid.csv", index=False)
    LV = pd.DataFrame(liverows).drop_duplicates()
    LV.to_csv(f"{OUT}.liveness.csv", index=False)
    P(f"   {len(GD)} grid rows written; {len(LV)} liveness rows")

    # ------------------------------------------------------- the liveness table
    P(f"\n{'='*118}\nTHE WARM-UP ACCOUNTING - how much of each PRE leg is the UNGATED book?"
      f"\n{'='*118}")
    P(f"   {'panel':<10}{'split':<12}" + "".join(f"{'w'+str(w):>12}" for w in WS_ROLL)
      + "   (share of the PRE leg on which the threshold EXISTS)")
    share_tab = {}
    for pname in PANELS:
        d = PAN[pname]
        for splitdate in SPLITS:
            cut = int(d["eidx"].searchsorted(pd.Timestamp(splitdate), side="right"))
            row = []
            for w in WS_ROLL:
                s = max(cut - d["live_w"][w], 0) / cut if cut else np.nan
                share_tab[(pname, splitdate, w)] = s
                row.append(s)
            P(f"   {pname:<10}{splitdate:<12}" + "".join(f"{x:>12.4f}" for x in row))

    # ------------------------------------------------------- the answer table
    def cellrow(rule, wsel, splitdate=SPLIT_HEAD, c=RUNG_HEAD, matching="FULLMATCH",
                scope="POOLED", stat="RAW", fam="QROLL"):
        q = GD[(GD.rule == rule) & (GD.wsel == str(wsel)) & (GD.split == splitdate)
               & (GD.rung == c) & (GD.matching == matching) & (GD.scope == scope)
               & (GD.stat == stat) & (GD.family == fam) & (GD.feasible)]
        return None if q.empty else q.iloc[0]

    def profile(rule, splitdate=SPLIT_HEAD, c=RUNG_HEAD, matching="FULLMATCH", scope="POOLED",
                stat="RAW", fam="QROLL"):
        out = {}
        for w in WS_ROLL:
            r = cellrow(rule, w, splitdate, c, matching, scope, stat, fam)
            out[w] = (np.nan, np.nan, np.nan, np.nan) if r is None else \
                (r.delta, r.p, r.win_PRE, r.win_POST)
        return out

    P(f"\n{'='*118}\nTHE ANSWER - QROLL's per-w delta under each leg rule (headline split "
      f"{SPLIT_HEAD}, {RUNG_HEAD:g} bps, FULLMATCH, POOLED)\n{'='*118}")
    P(f"   {'rule':<9}" + "".join(f"{'w'+str(w):>22}" for w in WS_ROLL)
      + f"{'spread':>9}{'rho(w,delta)':>14}")
    prof = {}
    for rule in RULES_LEG:
        pr = profile(rule)
        prof[rule] = pr
        cells = []
        for w in WS_ROLL:
            dlt, p, _, _ = pr[w]
            cells.append("n/a (leg too short)" if not np.isfinite(dlt)
                         else f"{dlt:+.4f} p{p:.4f}{'*' if p < ALPHA else ' '}")
        ds = np.array([pr[w][0] for w in WS_ROLL], float)
        sp = (np.nanmax(ds) - np.nanmin(ds)) if np.isfinite(ds).sum() >= 2 else np.nan
        rho = spearman(WS_ROLL, ds)
        P(f"   {rule:<9}" + "".join(f"{x:>22}" for x in cells)
          + f"{sp:>9.4f}{rho:>14.4f}")
    P(f"\n   {'rule':<9}" + "".join(f"{'w'+str(w)+' PRE/POST':>22}" for w in WS_ROLL))
    for rule in RULES_LEG:
        pr = prof[rule]
        P(f"   {rule:<9}" + "".join(
            (f"{'n/a':>22}" if not np.isfinite(pr[w][2])
             else f"{pr[w][2]:>10.4f} /{pr[w][3]:>10.4f}") for w in WS_ROLL))

    # the most recent split at which COMMON is feasible on all four w (for H_WINDOW)
    def all_feasible(rule, splitdate):
        return all(np.isfinite(profile(rule, splitdate)[w][0]) for w in WS_ROLL)

    common_ok = [s for s in SPLITS if all_feasible("COMMON", s)]
    live_ok = [s for s in SPLITS if all_feasible("LIVE", s)]
    P(f"\n   splits at which ALL FOUR w are feasible:  LIVE {live_ok or 'none'};  "
      f"COMMON {common_ok or 'none'};  RAW {[s for s in SPLITS if all_feasible('RAW', s)]}")
    SPLIT_CAL = common_ok[-1] if common_ok else None
    if SPLIT_CAL:
        P(f"   H_WINDOW is read on the LATEST all-feasible COMMON split: {SPLIT_CAL}")
        P(f"   {'rule':<9}" + "".join(f"{'w'+str(w):>22}" for w in WS_ROLL)
          + f"{'spread':>9}{'rho':>9}")
        for rule in RULES_LEG:
            pr = profile(rule, SPLIT_CAL)
            cells = [("n/a" if not np.isfinite(pr[w][0])
                      else f"{pr[w][0]:+.4f} p{pr[w][1]:.4f}{'*' if pr[w][1] < ALPHA else ' '}")
                     for w in WS_ROLL]
            ds = np.array([pr[w][0] for w in WS_ROLL], float)
            sp = (np.nanmax(ds) - np.nanmin(ds)) if np.isfinite(ds).sum() >= 2 else np.nan
            P(f"   {rule:<9}" + "".join(f"{x:>22}" for x in cells)
              + f"{sp:>9.4f}{spearman(WS_ROLL, ds):>9.4f}")

    # ------------------------------------------------------- H_LIVEFIT
    P(f"\n{'='*118}\nH_LIVEFIT - does LIVE SHARE explain the RAW delta better than log w?"
      f"\n{'='*118}")
    fitrows = []
    for pname in PANELS:
        for splitdate in SPLITS:
            for w in WS_ROLL:
                r = cellrow("RAW", w, splitdate, RUNG_HEAD, "FULLMATCH", pname, "RAW", "QROLL")
                if r is None:
                    continue
                fitrows.append(dict(panel=pname, split=splitdate, w=w, delta=r.delta,
                                    live=share_tab[(pname, splitdate, w)], logw=np.log(w)))
    FT = pd.DataFrame(fitrows)
    if len(FT) >= 6:
        P(f"   {len(FT)} (panel, split, w) cells with a RAW per-panel reading")
        P(f"   Spearman(delta, live share) {spearman(FT.delta, FT.live):+.4f}   "
          f"R^2 {r2(FT.live, FT.delta):.4f}")
        P(f"   Spearman(delta, log w)      {spearman(FT.delta, FT.logw):+.4f}   "
          f"R^2 {r2(FT.logw, FT.delta):.4f}")
        # partial: within live-share bands, is there still a w effect?
        hi = FT[FT.live >= 0.999]
        P(f"   restricted to FULLY LIVE cells (share >= 0.999): n = {len(hi)}, distinct w = "
          f"{sorted(hi.w.unique().tolist())}, Spearman(delta, log w) "
          f"{spearman(hi.delta, hi.logw):+.4f} "
          f"{'(undefined - only one w is ever fully live)' if hi.w.nunique() < 2 else ''}")
        livefit = (abs(spearman(FT.delta, FT.live)) >= abs(spearman(FT.delta, FT.logw))
                   and r2(FT.live, FT.delta) >= r2(FT.logw, FT.delta))
    else:
        livefit = False
        P("   too few cells")

    # ------------------------------------------------------- hypotheses
    P(f"\n{'='*118}\nPRE-REGISTERED HYPOTHESES\n{'='*118}")
    H = {}
    H["H_REPRO"] = (ok5, f"max|this run - 834's committed per-w delta| {g5:.2e} (bar 1e-12)")

    dsR = np.array([prof["RAW"][w][0] for w in WS_ROLL], float)
    rhoR = spearman(WS_ROLL, dsR)
    H["H_MONO_RAW"] = (rhoR == -1.0,
                       f"rho(w, delta) under RAW at the headline = {rhoR:+.4f} "
                       f"({' > '.join(f'{x:+.4f}' for x in dsR)})")

    spR = np.nanmax(dsR) - np.nanmin(dsR)
    dsL = np.array([prof["LIVE"][w][0] for w in WS_ROLL], float)
    nL = int(np.isfinite(dsL).sum())
    spL = (np.nanmax(dsL) - np.nanmin(dsL)) if nL >= 2 else np.nan
    H["H_WARMUP"] = (bool(np.isfinite(spL) and spL <= 0.5 * spR),
                     f"spread RAW {spR:.4f} -> LIVE {spL:.4f} "
                     f"({(1-spL/spR)*100:.1f}% shrink)" if np.isfinite(spL)
                     else f"spread RAW {spR:.4f}; LIVE has only {nL} of 4 w feasible at the "
                          f"headline split (the w>=1008 legs do not exist) - see the "
                          f"all-feasible split below")
    if SPLIT_CAL:
        pr = profile("COMMON", SPLIT_CAL)
        dsC = np.array([pr[w][0] for w in WS_ROLL], float)
        rhoC = spearman(WS_ROLL, dsC)
        prR = profile("RAW", SPLIT_CAL)
        dsRC = np.array([prR[w][0] for w in WS_ROLL], float)
        H["H_WINDOW"] = (rhoC == -1.0,
                         f"at {SPLIT_CAL} rho(w, delta) COMMON {rhoC:+.4f} "
                         f"({' '.join(f'{x:+.4f}' for x in dsC)}) vs RAW {spearman(WS_ROLL, dsRC):+.4f} "
                         f"({' '.join(f'{x:+.4f}' for x in dsRC)})")
        H["H_WARMUP_CAL"] = (
            bool((np.nanmax(dsC) - np.nanmin(dsC)) <= 0.5 * (np.nanmax(dsRC) - np.nanmin(dsRC))),
            f"at {SPLIT_CAL} spread RAW {np.nanmax(dsRC)-np.nanmin(dsRC):.4f} -> COMMON "
            f"{np.nanmax(dsC)-np.nanmin(dsC):.4f}")
    else:
        H["H_WINDOW"] = (False, "COMMON is feasible on all four w at NO split - the corpus cannot "
                                "hold the calendar fixed and keep every threshold alive")
    H["H_LIVEFIT"] = (bool(livefit),
                      f"Spearman |live| {abs(spearman(FT.delta, FT.live)):.4f} vs |log w| "
                      f"{abs(spearman(FT.delta, FT.logw)):.4f}; R^2 {r2(FT.live, FT.delta):.4f} vs "
                      f"{r2(FT.logw, FT.delta):.4f}" if len(FT) >= 6 else "too few cells")

    r2016_raw = cellrow("RAW", 2016)
    r2016_live = cellrow(RULE_HEAD, 2016)
    if r2016_live is None and SPLIT_CAL:
        r2016_live = cellrow(RULE_HEAD, 2016, SPLIT_CAL)
        note = f" (read at {SPLIT_CAL}; the headline split's LIVE leg is shorter than {MINLEG}d)"
    else:
        note = ""
    H["H_W2016SIG"] = (bool(r2016_live is not None and r2016_live.p < ALPHA),
                       f"w2016 RAW p {r2016_raw.p:.4f} -> {RULE_HEAD} "
                       f"{'n/a' if r2016_live is None else f'{r2016_live.p:.4f}'}{note}")

    def mono_verdict(rule, splitdate, c, matching, scope):
        ds = []
        for w in WS_ROLL:
            r = cellrow(rule, w, splitdate, c, matching, scope)
            ds.append(np.nan if r is None else float(r.delta))
        return spearman(WS_ROLL, np.array(ds, float))

    costv = [mono_verdict("RAW", SPLIT_HEAD, c, "FULLMATCH", "POOLED") for c in RUNGS]
    H["H_COSTINV"] = (len(set(np.round(costv, 6))) == 1,
                      "rho(w, delta) under RAW at " + ", ".join(f"{c:g}bps {v:+.4f}"
                                                                for c, v in zip(RUNGS, costv)))
    mv = [mono_verdict("RAW", SPLIT_HEAD, RUNG_HEAD, m, "POOLED") for m in MATCHINGS]
    H["H_MATCH"] = (len(set(np.round(mv, 6))) == 1,
                    ", ".join(f"{m} {v:+.4f}" for m, v in zip(MATCHINGS, mv)))
    pv = [mono_verdict("RAW", SPLIT_HEAD, RUNG_HEAD, "FULLMATCH", s) for s in PANELS]
    H["H_PANEL"] = (len({np.round(v, 6) for v in pv if np.isfinite(v)}) == 1,
                    ", ".join(f"{s} {v:+.4f}" for s, v in zip(PANELS, pv)))

    # H_R8CLAIM: pick the flattest-profile rule on the IS splits, read it on the OOS splits
    def spread_of(rule, splitdate):
        ds = np.array([profile(rule, splitdate)[w][0] for w in WS_ROLL], float)
        return (np.nanmax(ds) - np.nanmin(ds)) if np.isfinite(ds).sum() >= 2 else np.nan

    is_spread = {r: np.nanmean([spread_of(r, s) for s in SPLITS_IS]) for r in RULES_LEG}
    oos_spread = {r: np.nanmean([spread_of(r, s) for s in SPLITS_OOS]) for r in RULES_LEG}
    pick_rule = min((r for r in RULES_LEG if np.isfinite(is_spread[r])), key=lambda r: is_spread[r])
    flat_is = pick_rule != "RAW"
    flat_oos = (np.isfinite(oos_spread[pick_rule])
                and oos_spread[pick_rule] <= oos_spread["RAW"])
    H["H_R8CLAIM"] = (bool(flat_is and flat_oos),
                      "IS mean spread " + ", ".join(f"{r} {is_spread[r]:.4f}" for r in RULES_LEG)
                      + f" -> pick {pick_rule}; OOS mean spread "
                      + ", ".join(f"{r} {oos_spread[r]:.4f}" for r in RULES_LEG))

    # H_R8PICK: do the three choosers pick the same (level, w)?
    W = WF[~WF.no_candidate.astype(bool)] if "no_candidate" in WF.columns else WF
    piv = W.pivot_table(index=["panel", "rung", "family", "gross", "depth", "cadence"],
                        columns="chooser", values="w", aggfunc="first")
    qrows = piv.loc[piv.index.get_level_values("family") == "QROLL"] if len(piv) else piv
    if len(qrows) and {"BLIND", "LIVE50", "LIVELEG"} <= set(qrows.columns):
        diff50 = int((qrows.BLIND != qrows.LIVE50).sum())
        diffleg = int((qrows.BLIND != qrows.LIVELEG).sum())
        H["H_R8PICK"] = (bool(diff50 + diffleg > 0),
                         f"of {len(qrows)} QROLL (panel,rung,gross,depth,cadence) cells the "
                         f"warm-up-aware chooser moves the w pick in {diff50} (LIVE50) and "
                         f"{diffleg} (LIVELEG)")
    else:
        H["H_R8PICK"] = (False, "no QROLL picks to compare")

    for k, (okv, why) in H.items():
        P(f"   {k:<14} {'PASS' if okv else 'FAIL'}   {why}")

    # ------------------------------------------------------- rule 8 on the books
    P(f"\n{'='*118}\nPROTOCOL RULE 8 ON THE BOOKS - dial chosen on IS (..{IS_END}), OOS read ONCE"
      f"\n{'='*118}")
    LIVEW = (WF[~WF.no_candidate.astype(bool)].copy() if "no_candidate" in WF.columns
             else WF.copy())
    P(f"   {'chooser':<9}{'n':>5}{'4a':>5}{'4b':>5}{'med OOS Sharpe':>16}{'med OOS CAGR':>14}"
      f"{'med OOS MaxDD':>15}")
    for ch in ["BLIND", "LIVE50", "LIVELEG"]:
        s = LIVEW[LIVEW.chooser == ch]
        if s.empty:
            continue
        P(f"   {ch:<9}{len(s):>5}{int(s.pass_4a.sum()):>5}{int(s.pass_4b.sum()):>5}"
          f"{s.OOS_Sharpe.median():>16.3f}{s.OOS_CAGR.median():>14.2%}"
          f"{s.OOS_MaxDD.median():>15.2%}")
    b = LIVEW.iloc[0]
    P(f"   benchmarks on the SAME OOS window: RULES v2 {b.V2_OOS_CAGR:.2%} / "
      f"{b.V2_OOS_Sharpe:.3f} / {b.V2_OOS_MaxDD:.2%};  SPY {b.SPY_OOS_CAGR:.2%} / "
      f"{b.SPY_OOS_Sharpe:.3f} / {b.SPY_OOS_MaxDD:.2%}")
    P(f"\n   headline rung ({RUNG_HEAD:g} bps), QROLL only, per panel and chooser:")
    P(f"   {'panel':<10}{'chooser':<9}{'picks':>6}{'w picked (mode)':>18}{'4b':>4}{'4a':>4}"
      f"{'med OOS Sharpe':>16}{'vs v2':>8}{'vs SPY':>8}")
    for pname in PANELS:
        for ch in ["BLIND", "LIVE50", "LIVELEG"]:
            s = LIVEW[(LIVEW.panel == pname) & (LIVEW.chooser == ch)
                      & (LIVEW.family == "QROLL") & (LIVEW.rung == RUNG_HEAD)]
            if s.empty:
                continue
            md = s.OOS_Sharpe.median()
            P(f"   {pname:<10}{ch:<9}{len(s):>6}{str(sorted(s.w.mode().tolist())):>18}"
              f"{int(s.pass_4b.sum()):>4}{int(s.pass_4a.sum()):>4}{md:>16.3f}"
              f"{md - s.V2_OOS_Sharpe.iloc[0]:>8.3f}{md - s.SPY_OOS_Sharpe.iloc[0]:>8.3f}")

    P(f"\n   BOTH KEEP PATHS over all {len(AR)} (panel, arm, rung) rows:")
    P(f"      4a passes {int(AR.pass_4a.sum())} / {len(AR)}    "
      f"4b passes {int(AR.pass_4b.sum())} / {len(AR)}    "
      f"BOTH {int((AR.pass_4a & AR.pass_4b).sum())}")
    fb = AR[~AR.pass_4b].fail_4b.value_counts().head(6)
    P("      4b binding legs: " + ", ".join(f"{k} {v}" for k, v in fb.items()))
    if int(AR.pass_4b.sum()):
        bp = AR[AR.pass_4b]
        P(f"      4b passers by panel: " + ", ".join(f"{k} {v}" for k, v in
                                                     bp.panel.value_counts().items()))
        P(f"      of them, twin (matched-gross static) ALSO passes 4b: "
          f"{int(bp.twin_pass_4b.sum())} / {len(bp)} "
          f"=> {len(bp) - int(bp.twin_pass_4b.sum())} are clause-attributable")
    r8_4b = int(LIVEW.pass_4b.sum())
    r8_4a = int(LIVEW.pass_4a.sum())
    P(f"      rule-8 picks: 4b {r8_4b} / {len(LIVEW)}, 4a {r8_4a} / {len(LIVEW)}")
    if r8_4b:
        best = LIVEW[LIVEW.pass_4b].sort_values("OOS_Sharpe", ascending=False).iloc[0]
        P(f"      best rule-8 4b passer: {best.panel} {best.family} L{best.level} w{best.w} "
          f"d{best.depth} {best.cadence} g{best.gross} rung {best.rung:g} chooser {best.chooser} "
          f"-> OOS {best.OOS_CAGR:.2%} / {best.OOS_Sharpe:.3f} / {best.OOS_MaxDD:.2%} vs v2 "
          f"{best.V2_OOS_CAGR:.2%}/{best.V2_OOS_Sharpe:.3f} vs SPY {best.SPY_OOS_CAGR:.2%}/"
          f"{best.SPY_OOS_Sharpe:.3f}")

    # ------------------------------------------------------- verdict
    P(f"\n{'='*118}\nVERDICT\n{'='*118}")
    P("   GATES: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in GATES.items()))
    npass = sum(1 for v in H.values() if v[0])
    P(f"   HYPOTHESES: {npass} of {len(H)} PASS")
    P(f"   grid points reported: {len(GD)} rows over {len(WSELS)}x{len(RULES_LEG)} tuned points "
      f"x {len(SPLITS)} splits x {len(RUNGS)} rungs x {len(MATCHINGS)} matchings x "
      f"{len(SCOPES)} scopes x {len(STATS)} statistics")
    P(f"   elapsed {time.time()-T0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(G=GATES, H=H, GD=GD, AR=AR, WF=LIVEW, prof=prof, share=share_tab,
                SPLIT_CAL=SPLIT_CAL, FT=FT)


if __name__ == "__main__":
    main()

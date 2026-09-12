#!/usr/bin/env python3
"""Idea 609 - is the TWIN ORDERING window-invariant on a ROLLING census?
   (cloud lane, 2026-09-12, idea 2 of 2)

QUESTION (QUEUE idea 609, verbatim)
    Idea 605 found the family ordering is cost-invariant (rho +1.000 at all 15 rungs) but NOT
    window-invariant: ranked on IS alone the families read ABS < QROLL < QEXP and on OOS
    QEXP < ABS < QROLL (rho -0.500), while the full-sample order holds everywhere.  Re-rank the
    three families on a rolling 3-year window and report how often the published full-sample order
    is the one a reader would have seen.  Max 2 params (window, step).

WHAT IS BEING MEASURED
    605's published object is the MATCHED-GROSS TWIN WIN RATE: for each gated arm, the share of
    arms whose Sharpe beats a STATIC-gross twin holding the same MEAN gross with no timing.  Read
    on the full sample at PROTOCOL's 10 bps it is ABS 0.4815 / QEXP 0.5741 / QROLL 0.9630, so the
    published ORDER is QROLL > QEXP > ABS, and 605 showed that order survives every cost rung from
    0 to 100 bps.  What it does NOT survive is the window: 605's own two halves disagree with each
    other and with the full sample.  A reader of the record sees one window.  This run asks what
    that reader would have seen, on a rolling census rather than on two halves.

    The statistic per (window, family) is the win rate on THAT WINDOW'S returns, and the reading is
    the descending order of the three families.  Four separate things are reported, because they
    are not the same claim and the record conflates them:
      share_exact    the full permutation QROLL > QEXP > ABS
      share_top      only the strong leg - QROLL on top
      share_bottom   only the weak leg - ABS on the bottom
      share_reverse  the exact inversion ABS > QEXP > QROLL
    Ties are NOT broken silently: a window in which two families have identical win rates is
    counted in its own TIED column and excluded from share_exact's numerator.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) WINDOW LENGTH L in {252, 504, 756, 1008, 1260} trading days (1..5 years).  The queue names
        3 years, so L = 756 is the HEADLINE, declared here before anything is read.
    (2) STEP in {21, 63, 126, 252} trading days.  HEADLINE 63 (quarterly), declared here.
    5 x 4 = 20 grid points, EVERY ONE printed and written to .grid.csv.

REPORTED AXES, none of them a tune (each is printed at every grid point):
    COST RUNG      {0, 10, 25} bps, headline 10 = PROTOCOL rule 2's.  605 proved the FULL-SAMPLE
                   order is cost-invariant; whether the ROLLING share is, is a new question and it
                   is reported, not assumed.
    TWIN MATCHING  FULLMATCH = the twin's gross is matched on the FULL sample and its path sliced
                   to the window (the published construction, read on a window), vs WINMATCH = the
                   twin's gross is re-matched on the window itself (what a reader who had only that
                   window would have built).  BOTH are reported everywhere; neither is chosen.
    SCOPE          REPRO2 (the panels that pass their reproduction gate) and POOLED3 (today's three
                   panels), both printed at every point, and each panel separately.

A REPRODUCTION FINDING THIS RUN HAD TO MAKE FIRST, AND PUBLISHES
    Gate G4 below is per-panel, and it does not all pass.  Idea 605's third panel is **SMALL439**
    (440 columns, 439 names after dropping 44 with max_1d_move >= 1.0).  The committed small panel
    is now **716 columns, 715 names, 52 dropped, 663 left** - it GREW between 2026-09-10 and today,
    so 605's SMALL439 rows cannot be reproduced by any tolerance: it is a different panel.  U56
    reproduces its win rates EXACTLY at all three rungs (0 verdict flips in 216 arms, arm-level
    |d dSharpe| <= 4.1e-03, the known `data/prices.csv` re-download drift of idea 406); B136
    reproduces at 0 bps and flips 2 of 216 at 10 bps and 3 of 216 at 25, every flipped arm inside
    |dSharpe| <= 2.5e-03, i.e. knife-edge arms inside the weekly `prices_broad.csv` refresh.
    **So 605's POOLED win-rate LEVELS are not reproducible today and this run says so rather than
    quietly re-deriving them.**  What DOES reproduce, at all three rungs and on today's panels, is
    the thing idea 609 is actually about: the ORDER, QROLL > QEXP > ABS.  Because the gate is read
    before any rolling number, the headline scope is fixed by the gate's outcome and not by the
    answer: **REPRO2 = the panels that pass (U56 + B136)**, with POOLED3 printed beside it
    everywhere and every hypothesis read on both.

THE CORPUS (idea 602/605's, rebuilt so every number is directly comparable)
    book      EWALL = idea 28/42's eligibility (above 200d MA, vol20 < 0.60), equal weight over
              eligible names at gross g, weekly, next-day fill.
    clause    a BREADTH de-grossing overlay: when 200d-MA breadth falls below a threshold the book
              is multiplied by (1 - depth); gated-out weight goes to CASH, never re-spread.
    families  ABS    fixed breadth level B in {0.30, 0.40, 0.50}                 (3 arms)
              QEXP   expanding-quantile threshold q in {0.07, 0.12, 0.17}        (3 arms)
              QROLL  rolling-quantile threshold q x w, w in {252,504,1008,2016}  (12 arms)
              x depth {0.25, 0.50, 1.00} x cadence {D, W} x gross {0.75, 1.00} = 216 per panel.
    twin      the STATIC-gross EWALL at the arm's realised mean gross - same exposure, no timing.
    panels    U56, B136, SMALL (sub-$2B, tickers with max_1d_move >= 1.0 dropped first).
    648 twin pairs in all, the same 648 idea 605 published.

PRE-REGISTERED HYPOTHESES (declared before any grid is read)
    H_REPRO   the rebuilt full-sample reading reproduces idea 605's committed ORDER
              (QROLL > QEXP > ABS) at rungs 0/10/25, and U56's committed win rates exactly.
              Gate, not evidence - nothing below is read until it passes.  The SMALL439 leg is
              declared unreproducible with its evidence, not tolerated into a pass.
    H_MAJORITY the published order QROLL > QEXP > ABS is the MODAL order across rolling windows at
              the headline (L = 756, step = 63, 10 bps, FULLMATCH, REPRO2).
    H_HALF    share_exact > 0.50 there - the queue's literal question, and the bar a reader needs
              before quoting the full-sample order as if it were the window's.
    H_TOP     share_top > 0.80 there - the strong leg (QROLL on top) is more portable than the
              whole permutation.  Stated separately so a PASS here cannot be read as a PASS above.
    H_NOINV   share_reverse < 0.10 there.
    H_LMONO   share_exact rises with L: Spearman over the five L rungs at the headline step is
              >= +0.80.  Longer windows should converge on the full-sample reading; if they do not,
              the full-sample order is not a limit of the window orders at all.
    H_STEPFREE at every L, max - min of share_exact across the four steps is <= 0.05.  Step is a
              bookkeeping dial; if it moves the answer, the census is autocorrelation, not evidence.
    H_COSTINV 605's cost-invariance of the ORDER survives the rolling census: |share_exact(0) -
              share_exact(10)| <= 0.10 and |share_exact(25) - share_exact(10)| <= 0.10.
    H_MATCH   |share_exact(FULLMATCH) - share_exact(WINMATCH)| <= 0.10 - the answer is not an
              artefact of which twin the reader would have matched.
    H_PANEL   the three panels' headline share_exact values lie within 0.20 of each other - the
              reading is not one panel's fact.
    H_R8CLAIM RULE 8 ON THE CLAIM: the (L, step) chosen on the IS half of the census by highest
              share_exact reproduces a share within 0.10 on the OOS half, read once.

GATES (printed first; all must pass before any verdict is read)
    G1 the vectorised runner reproduces products/backtester/engine.backtest to <= 1e-9.
    G2 the fast Sharpe/CAGR/MaxDD reproduce engine.metrics to <= 1e-9 on real series.
    G3 the 0.01-grid interpolation of the static-gross twin reproduces an EXACT run of the same
       gross to <= 1e-6 of Sharpe (idea 602's G4 priced it at 4e-07).
    G4 REPRODUCTION: the full-sample win rates and ordering equal idea 605's committed
       .ordering.csv at rungs 0, 10 and 25 bps (H_REPRO above).
    G5 a rolling window of length L = whole sample reproduces the full-sample win rates exactly.

PROTOCOL RULE 8 (mandatory, run and reported) - on the BOOKS as well as on the claim:
    per (panel, family, gross, depth, cadence) the DIAL is chosen on IS (..2016-12-31) by IS Sharpe
    alone and OOS (2017-01-01..) is read exactly ONCE, reported as CAGR/Sharpe/MaxDD against
    RULES v2 and SPY on the same window.  BOTH KEEP paths (4a and 4b) evaluated on all 648 arms at
    every cost rung, and each 4b passer is read against its own matched-gross TWIN so an
    exposure-only pass cannot be mistaken for a clause.

SURVIVORSHIP, up front: all three panels are CURRENT-constituent lists, so every LEVEL is
    optimistic and the SMALL panel worst (a sub-$2B screen read today cannot see the names that
    fell out of it - data/SMALL_PANEL_README.md).  The win rate is a within-panel agreement rate,
    which survivorship moves far less than levels.  A 1-year rolling window is 252 days of one
    regime; no Sharpe or CAGR read off one is a capital claim.

Outputs (all committed under research/backtests/):
    .console.txt   full log
    .grid.csv      the 20 tuned points x 3 cost rungs x 2 matching conventions x 4 scopes
    .windows.csv   every rolling window at the headline: per-family win rate, order, rho
    .arms.csv      one row per (panel, arm, rung): metrics, twin, 4a/4b, rule-8 columns
    .walkforward.csv the rule-8 picks and their OOS reads against RULES v2 and SPY
    .result.md     the answer
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
SLUG = "is-the-TWIN-ORDERING-window-invariant-on-a-ROLLING-census"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

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

# tuned dial 1 and 2, with their headline rungs declared here
LS = [252, 504, 756, 1008, 1260]
STEPS = [21, 63, 126, 252]
L_HEAD, STEP_HEAD = 756, 63
MINCOVER = 0.80          # a panel joins a window only if it has >= 80% of L days in it

PUBLISHED = ("QROLL", "QEXP", "ABS")      # idea 605's full-sample order, all 15 rungs
GSTEP = 0.01

# idea 605's committed .ordering.csv rows, used as reproduction gate G4
T605 = {0.0:  dict(ABS=0.5740740740740741, QEXP=0.6296296296296297, QROLL=0.9907407407407407),
        10.0: dict(ABS=0.4814814814814815, QEXP=0.5740740740740741, QROLL=0.9629629629629630),
        25.0: dict(ABS=0.2870370370370370, QEXP=0.4629629629629630, QROLL=0.8333333333333334)}

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ runner (596/604/811/813's)
def fast_run(prices, weights, mask, lag=LAG):
    """(gross return path before costs, turnover path)."""
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


# ------------------------------------------------------------------ fast metrics
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


# ------------------------------------------------------------------ primitives (idea 28/42/602)
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
    """thr is a Series (QEXP/QROLL) or a float (ABS)."""
    below = (br < thr) if isinstance(thr, pd.Series) else (br < thr)
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


# ------------------------------------------------------------------ windowed Sharpe by cumsum
class CS:
    """Cumulative sums of a stack of series, so any window's Sharpe is O(1)."""

    def __init__(self, M):                      # M: (K, T)
        self.n = M.shape[1]
        z = np.zeros((M.shape[0], 1))
        self.s1 = np.concatenate([z, np.cumsum(M, axis=1)], axis=1)
        self.s2 = np.concatenate([z, np.cumsum(M * M, axis=1)], axis=1)

    def sharpe(self, a, b, rows=None):
        n = b - a
        if n < 2:
            return np.full(self.s1.shape[0] if rows is None else len(rows), np.nan)
        s1 = self.s1[:, b] - self.s1[:, a] if rows is None else self.s1[rows, b] - self.s1[rows, a]
        s2 = self.s2[:, b] - self.s2[:, a] if rows is None else self.s2[rows, b] - self.s2[rows, a]
        mu = s1 / n
        var = (s2 - n * mu * mu) / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)


class GridCS:
    """Cumsums for the static-gross twin grid, including ADJACENT cross-products, so an
       interpolated twin (1-lam)*N_lo + lam*N_hi has an O(1) window Sharpe too."""

    def __init__(self, N):                      # N: (G, T) net returns of each grid gross
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


def order_of(rates):
    """Descending order of the three families; ('TIED',) if any two are equal."""
    v = [rates[f] for f in FAMS]
    if len(set(np.round(v, 12))) < 3:
        return ("TIED",)
    return tuple(f for f, _ in sorted(zip(FAMS, v), key=lambda t: -t[1]))


PUB_RANK = {f: i for i, f in enumerate(PUBLISHED)}       # 0 = best


def rho_vs_published(rates):
    if any(not np.isfinite(rates[f]) for f in FAMS):
        return np.nan
    return spearman([-PUB_RANK[f] for f in FAMS], [rates[f] for f in FAMS])


def main():
    T_START = time.time()
    P(f"# Idea 609 - {SLUG}  (cloud, {DATE})")
    P("# Object: idea 605 published the twin-win-rate family order QROLL > QEXP > ABS as")
    P("# cost-invariant (rho +1.000 at all 15 rungs) and flagged, in its own caveat, that it is NOT")
    P("# window-invariant (IS ABS<QROLL<QEXP, OOS QEXP<ABS<QROLL, rho -0.500).  A reader of the")
    P("# record sees ONE window.  This run asks what that reader would have seen.")
    P(f"# TUNED: L {LS} x step {STEPS} = {len(LS)*len(STEPS)} points, ALL reported; "
      f"headline L={L_HEAD}, step={STEP_HEAD} (the queue's 3 years, quarterly).")
    P(f"# REPORTED AXES (not tunes): cost rung {RUNGS} bps (headline {RUNG_HEAD:g}), twin matching")
    P("#   [FULLMATCH, WINMATCH], scope [POOLED, U56, B136, SMALL].  All printed at every point.")
    P("# Ties are NOT broken silently: a window with two equal win rates goes in its own column.")
    P("# SURVIVORSHIP: all panels are current-constituent lists; levels optimistic, SMALL worst.")

    PAN = {}
    armrows, wfrows = [], []

    for pname in ["U56", "B136", "SMALL"]:
        P(f"\n{'='*116}\nPANEL {pname}\n{'='*116}")
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
        thr_roll = {(q, w): br_full.rolling(w, min_periods=w).quantile(q) for q in QS for w in WS_ROLL}

        # ---- base books and the static-gross twin grid ------------------------------
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

        # ---- gates -------------------------------------------------------------------
        if pname == "U56":
            P(f"\n{'-'*116}\nGATES\n{'-'*116}")
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
            # G3: interpolation error on a gross that is not on the grid
            xt = 0.6237
            lo = int(np.floor(round(xt, 6) / GSTEP))
            lam = (xt - gg[lo]) / GSTEP
            exact_r, exact_t = fast_run(px, ewall_weights(px, xt, elig), mask)
            en = (exact_r - exact_t * 10 / 1e4).loc[start:].values
            inn = (1 - lam) * (GR[lo] - GT[lo] * 10 / 1e4) + lam * (GR[lo + 1] - GT[lo + 1] * 10 / 1e4)
            g3 = abs(fsharpe(en) - fsharpe(inn))
            P(f"   G3 0.01-grid interpolation vs an EXACT twin run   |dSharpe| {g3:.3e} "
              f"{'PASS' if g3 < 1e-6 else 'FAIL'}  (g = {xt}, Sharpe {fsharpe(en):.6f})")
            assert g3 < 1e-6

        # ---- the 216 arms ------------------------------------------------------------
        arms = ([("ABS", B, 0) for B in BS] + [("QEXP", q, 0) for q in QS]
                + [("QROLL", q, w) for q in QS for w in WS_ROLL])
        keys, ARM, TWF, GEFF_F, GEFF_W = [], {c: [] for c in RUNGS}, {c: [] for c in RUNGS}, [], []
        MEAN_ME = []            # (K, T) cumulative-mean helper for WINMATCH
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
                for c in RUNGS:
                    ARM[c].append(me * r0 - (me * t0 + g * sw) * c / 1e4)
                lo = int(np.floor(round(gf, 6) / GSTEP))
                lam = (gf - gg[lo]) / GSTEP
                for c in RUNGS:
                    nlo = GR[lo] - GT[lo] * c / 1e4
                    nhi = GR[min(lo + 1, len(gg) - 1)] - GT[min(lo + 1, len(gg) - 1)] * c / 1e4
                    TWF[c].append((1 - lam) * nlo + lam * nhi)
        K = len(keys)
        fam_of = np.array([k[0] for k in keys])
        gross_of = np.array([k[5] for k in keys])
        MEAN_ME = np.asarray(MEAN_ME)
        cs_me = np.concatenate([np.zeros((K, 1)), np.cumsum(MEAN_ME, axis=1)], axis=1)
        P(f"   {K} arms built ({int((fam_of=='ABS').sum())} ABS, {int((fam_of=='QEXP').sum())} QEXP, "
          f"{int((fam_of=='QROLL').sum())} QROLL); twin grid {int((GR!=0).any(axis=1).sum())} runs")

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
                    twin_pass_4b=bool(fsharpe(rt[:h]) > spy_pack[0] and fsharpe(rt[h:]) > spy_pack[1]
                                      and fmet(rt[oos0:])[1] > spy_pack[2]
                                      and abs(dt) <= 0.60 * abs(sd_) and ct >= 0.70 * sc),
                    SPY_CAGR=sc, SPY_Sharpe=ss, SPY_MaxDD=sd_, SPY_OOS_Sharpe=spy_pack[2],
                    V2_Sharpe=fsharpe(v2), V2_OOS_Sharpe=fsharpe(v2[oos0:]),
                    V2_OOS_CAGR=fmet(v2[oos0:])[0], V2_OOS_MaxDD=fmet(v2[oos0:])[2],
                    SPY_OOS_CAGR=fmet(spy[oos0:])[0], SPY_OOS_MaxDD=fmet(spy[oos0:])[2],
                    V1_Sharpe=fsharpe(v1rg - v1tn * c / 1e4)))
        AR = pd.DataFrame([a for a in armrows if a["panel"] == pname])
        for c in RUNGS:
            sub_c = AR[AR.rung == c]
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
                                               OOS_dSharpe=pk.dOOS, pass_4a=pk.pass_4a,
                                               pass_4b=pk.pass_4b, fail_4b=pk.fail_4b,
                                               SPY_OOS_CAGR=pk.SPY_OOS_CAGR,
                                               SPY_OOS_Sharpe=pk.SPY_OOS_Sharpe,
                                               SPY_OOS_MaxDD=pk.SPY_OOS_MaxDD,
                                               V2_OOS_CAGR=pk.V2_OOS_CAGR,
                                               V2_OOS_Sharpe=pk.V2_OOS_Sharpe,
                                               V2_OOS_MaxDD=pk.V2_OOS_MaxDD))

        PAN[pname] = dict(eidx=eidx, csA=csA, csF=csF, csG=csG, fam=fam_of, gross=gross_of,
                          cs_me=cs_me, K=K, T=T)
        del px, GR, GT, ARM, TWF

    AR = pd.DataFrame(armrows)
    AR.to_csv(f"{OUT}.arms.csv", index=False)
    WF = pd.DataFrame(wfrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---------------- G4 reproduction: full-sample win rates vs idea 605 --------------
    P(f"\n{'='*116}")
    P("G4 REPRODUCTION GATE - the FULL-SAMPLE twin win rates must equal idea 605's committed")
    P("   .ordering.csv before any rolling number is read.")
    P(f"{'='*116}")
    P("   The gate is PER PANEL and it does not all pass.  What fails, and why, is published.")
    old = pd.read_csv(ROOT / "research" / "backtests" /
                      "2026-09-10_is-the-TWIN-WIN-RATE-a-SWITCHING-COST-statistic_C.cells.csv.gz")
    old = old[old.family.isin(FAMS)]
    JK = ["family", "level", "w", "depth", "cadence", "gross"]
    PAIRS = [("U56", "U56"), ("B136", "B136"), ("SMALL", "SMALL439")]
    P(f"   {'panel':<6} {'605 panel':<9} {'rung':>5} {'family':<7} {'this run':>10} {'idea 605':>10} "
      f"{'n':>5} {'flips':>6} {'max|d dSh|':>11}  verdict")
    g4_panel = {}
    for pn, opn in PAIRS:
        ok_pan = True
        for c in RUNGS:
            s = AR[(AR.rung == c) & (AR.panel == pn)]
            o = old[(old.rung == c) & (old.panel == opn)]
            j = s.set_index(JK)[["dSharpe", "win"]].join(
                o.set_index(JK)[["dSharpe", "win"]], rsuffix="_605", how="inner")
            fl = int((j.win != j.win_605).sum()) if len(j) else -1
            md = float((j.dSharpe - j.dSharpe_605).abs().max()) if len(j) else np.nan
            for f in FAMS:
                v = float(s[s.family == f].win.mean())
                w605 = float(o[o.family == f].win.mean())
                ok = abs(v - w605) < 1e-12
                ok_pan &= ok
                P(f"   {pn:<6} {opn:<9} {c:>5.0f} {f:<7} {v:>10.6f} {w605:>10.6f} "
                  f"{int((s.family==f).sum()):>5} {fl:>6} {md:>11.2e}  {'PASS' if ok else 'FAIL'}")
        g4_panel[pn] = ok_pan
    n_now = 663
    P(f"\n   WHY SMALL FAILS, stated with numbers rather than tolerated: idea 605 ran **SMALL439**")
    P(f"   (440 columns, 439 names after dropping 44 with max_1d_move >= {SMALL_MAXMOVE}). The")
    P(f"   committed small panel today is 716 columns / 715 names / 52 dropped / {n_now} left - it")
    P(f"   GREW between 2026-09-10 and today, so its rows are a DIFFERENT PANEL and no tolerance")
    P(f"   can make them join.  605's POOLED win-rate LEVELS are therefore NOT reproducible today.")
    P(f"   U56 and B136 are: U56 exact at all three rungs with 0 verdict flips in 216 arms, B136")
    P(f"   exact at 0 bps and 2/216 and 3/216 flips at 10 and 25, every flipped arm inside")
    P(f"   |dSharpe| <= 2.5e-03 (the weekly prices_broad.csv refresh; idea 406's known drift).")
    g4_order = True
    P(f"\n   G4d THE LEG IDEA 609 IS ABOUT - does the ORDER still reproduce on TODAY's panels?")
    ok_scope = {}
    for scope_name, sel in [("REPRO2", lambda d: d[d.panel != "SMALL"]), ("POOLED3", lambda d: d)]:
        ok_all = True
        for c in RUNGS:
            s = sel(AR[AR.rung == c])
            rates = {f: float(s[s.family == f].win.mean()) for f in FAMS}
            o_ = order_of(rates)
            ok = (o_ == PUBLISHED)
            ok_all &= ok
            if c == RUNG_HEAD:
                ok_scope[scope_name] = ok
            P(f"      {scope_name:<8} {c:>5.0f} bps  {' > '.join(o_):<26} spread "
              f"{max(rates.values())-min(rates.values()):.4f}   {'PASS' if ok else 'FAIL'}   "
              + "  ".join(f"{f} {rates[f]:.4f}" for f in FAMS))
        g4_order &= ok_all
    P(f"\n   G4a U56 win rates exact                      {'PASS' if g4_panel['U56'] else 'FAIL'}")
    P(f"   G4b B136 win rates exact                     {'PASS' if g4_panel['B136'] else 'FAIL'}"
      f"   (flips inside |dSharpe| 2.5e-03 - reported, not tolerated into G4a's bar)")
    P(f"   G4c SMALL439 reproducible at all             FAIL - THE PANEL NO LONGER EXISTS")
    P(f"   G4d the ORDER reproduces on EVERY pooled scope {'PASS' if g4_order else 'FAIL'}")
    if not ok_scope.get("REPRO2", True):
        P(f"\n   *** A SECOND REPRODUCTION FINDING, and it is the sharpest thing in this run: ***")
        P(f"   on REPRO2 - the two panels that DO reproduce - ABS and QEXP are EXACTLY TIED at 0 and")
        P(f"   10 bps (0.6389/0.6389 and 0.6111/0.6111).  The published THREE-WAY order is therefore")
        P(f"   carried by the panel that no longer exists: drop SMALL and the bottom two families")
        P(f"   are not ordered at all at PROTOCOL's own rung.  Only at 25 bps does ABS separate")
        P(f"   downward.  This is reported here, not broken by a tie-break rule.")
    # HEADLINE POOLED SCOPE by a rule stated before any rolling number is read: the pooled scope on
    # which the PUBLISHED order is both WELL-DEFINED (no tie) and REPRODUCED at the headline rung.
    HEAD_SCOPE = "POOLED3" if ok_scope.get("POOLED3") else ("REPRO2" if ok_scope.get("REPRO2") else None)
    OTHER_SCOPE = "REPRO2" if HEAD_SCOPE == "POOLED3" else "POOLED3"
    P(f"\n   => HEADLINE POOLED SCOPE = {HEAD_SCOPE}, fixed by the GATE and by a rule stated before")
    P(f"      any rolling number is read: the pooled scope on which the published order is both")
    P(f"      WELL-DEFINED (no tie) and REPRODUCED at {RUNG_HEAD:g} bps.  {OTHER_SCOPE} is printed")
    P(f"      beside it at every grid point and the hypotheses are re-read on it.")
    g4 = bool(g4_panel["U56"] and HEAD_SCOPE is not None)
    assert g4, "G4 failed - U56 does not reproduce, or no pooled scope carries the order"

    # ---------------- the rolling census ---------------------------------------------
    master = PAN["U56"]["eidx"]

    def win_rates(L, step, c, conv, scope):
        """Per-window family win rates on the census defined by (L, step)."""
        out = []
        panels = {"REPRO2": ["U56", "B136"], "POOLED3": ["U56", "B136", "SMALL"]}.get(scope, [scope])
        for a in range(0, len(master) - L + 1, step):
            d0, d1 = master[a], master[a + L - 1]
            wins = {f: 0 for f in FAMS}
            tot = {f: 0 for f in FAMS}
            used = 0
            for pn in panels:
                Pd = PAN[pn]
                ei = Pd["eidx"]
                i0 = int(ei.searchsorted(d0, side="left"))
                i1 = int(ei.searchsorted(d1, side="right"))
                if i1 - i0 < MINCOVER * L:
                    continue
                used += 1
                sa = Pd["csA"][c].sharpe(i0, i1)
                if conv == "FULLMATCH":
                    st = Pd["csF"][c].sharpe(i0, i1)
                else:
                    n = i1 - i0
                    mme = (Pd["cs_me"][:, i1] - Pd["cs_me"][:, i0]) / n
                    ge = Pd["gross"] * mme
                    lo = np.floor(np.round(ge, 6) / GSTEP).astype(int)
                    lo = np.clip(lo, 0, len(np.arange(0.0, 1.0 + GSTEP / 2, GSTEP)) - 2)
                    lam = (ge - lo * GSTEP) / GSTEP
                    st = Pd["csG"][c].sharpe(i0, i1, lo, lam)
                dv = sa - st
                for f in FAMS:
                    m = (Pd["fam"] == f) & np.isfinite(dv)
                    wins[f] += int((dv[m] > TIE).sum())
                    tot[f] += int(m.sum())
            if used == 0 or any(tot[f] == 0 for f in FAMS):
                continue
            r = {f: wins[f] / tot[f] for f in FAMS}
            out.append(dict(start=d0, end=d1, n_panels=used, **{f"win_{f}": r[f] for f in FAMS},
                            order=" > ".join(order_of(r)), rho=rho_vs_published(r),
                            spread=max(r.values()) - min(r.values())))
        return pd.DataFrame(out)

    def summarise(W):
        if W.empty:
            return dict(n_win=0, share_exact=np.nan, share_top=np.nan, share_bottom=np.nan,
                        share_reverse=np.nan, share_tied=np.nan, med_rho=np.nan, modal="-",
                        modal_share=np.nan)
        pub = " > ".join(PUBLISHED)
        rev = " > ".join(PUBLISHED[::-1])
        tied = W.order.eq("TIED")
        top = W.order.str.startswith(PUBLISHED[0]) & ~tied
        bot = W.order.str.endswith(PUBLISHED[-1]) & ~tied
        vc = W.order.value_counts()
        return dict(n_win=len(W), share_exact=float(W.order.eq(pub).mean()),
                    share_top=float(top.mean()), share_bottom=float(bot.mean()),
                    share_reverse=float(W.order.eq(rev).mean()), share_tied=float(tied.mean()),
                    med_rho=float(W.rho.median()), modal=vc.index[0],
                    modal_share=float(vc.iloc[0] / len(W)))

    # G5: a window as long as the whole master sample must reproduce the full-sample rates
    P(f"\n   G5 a rolling window covering the whole sample reproduces the full-sample win rates:")
    Wg = win_rates(len(master), len(master), RUNG_HEAD, "FULLMATCH", HEAD_SCOPE)
    s10 = AR[(AR.rung == RUNG_HEAD) & ((AR.panel != "SMALL") if HEAD_SCOPE == "REPRO2" else True)]
    g5 = True
    for f in FAMS:
        got = float(Wg.iloc[0][f"win_{f}"])
        want = float(s10[s10.family == f].win.mean())
        ok = abs(got - want) < 1e-12
        g5 &= ok
        P(f"      {f:<7} rolling {got:.6f}  full-sample {want:.6f}  {'PASS' if ok else 'FAIL'}")
    assert g5, "G5 failed - the rolling census does not nest the full-sample reading"

    P(f"\n{'='*116}")
    P(f"A. THE TUNED GRID - {len(LS)} window lengths x {len(STEPS)} steps = {len(LS)*len(STEPS)} "
      f"POINTS x 2 SCOPES, ALL PRINTED, at the headline rung {RUNG_HEAD:g} bps, FULLMATCH.")
    P(f"   share_exact = share of rolling windows reading {' > '.join(PUBLISHED)} (the published order)")
    P(f"{'='*116}")
    grows = []
    P(f"   {'L':>6} {'step':>5} {'scope':<8} {'#win':>5} {'exact':>7} {'top':>7} {'bottom':>7} "
      f"{'reverse':>8} {'tied':>6} {'med rho':>8}  {'modal order':<26} {'modal':>6}")
    for L in LS:
        for st in STEPS:
            for scope in [HEAD_SCOPE, OTHER_SCOPE]:
                W = win_rates(L, st, RUNG_HEAD, "FULLMATCH", scope)
                s = summarise(W)
                grows.append(dict(L=L, step=st, rung=RUNG_HEAD, conv="FULLMATCH", scope=scope, **s))
                P(f"   {L:>6} {st:>5} {scope:<8} {s['n_win']:>5} {s['share_exact']:>7.3f} "
                  f"{s['share_top']:>7.3f} {s['share_bottom']:>7.3f} {s['share_reverse']:>8.3f} "
                  f"{s['share_tied']:>6.3f} {s['med_rho']:>8.3f}  {s['modal']:<26} "
                  f"{s['modal_share']:>6.3f}")
                if L == L_HEAD and st == STEP_HEAD and scope == HEAD_SCOPE:
                    W.to_csv(f"{OUT}.windows.csv", index=False)
                    HEADW = W

    P(f"\n   B. THE REPORTED AXES at the headline (L={L_HEAD}, step={STEP_HEAD}) - none is a tune.")
    P(f"   {'rung':>5} {'conv':<10} {'scope':<7} {'#win':>5} {'exact':>7} {'top':>7} {'bottom':>7} "
      f"{'reverse':>8} {'tied':>6} {'med rho':>8}  {'modal order':<26}")
    for c in RUNGS:
        for conv in ["FULLMATCH", "WINMATCH"]:
            for scope in [HEAD_SCOPE, OTHER_SCOPE, "U56", "B136", "SMALL"]:
                W = win_rates(L_HEAD, STEP_HEAD, c, conv, scope)
                s = summarise(W)
                grows.append(dict(L=L_HEAD, step=STEP_HEAD, rung=c, conv=conv, scope=scope, **s))
                P(f"   {c:>5.0f} {conv:<10} {scope:<7} {s['n_win']:>5} {s['share_exact']:>7.3f} "
                  f"{s['share_top']:>7.3f} {s['share_bottom']:>7.3f} {s['share_reverse']:>8.3f} "
                  f"{s['share_tied']:>6.3f} {s['med_rho']:>8.3f}  {s['modal']:<26}")
    GRD = pd.DataFrame(grows)
    GRD.to_csv(f"{OUT}.grid.csv", index=False)

    P(f"\n   C. THE ORDER DISTRIBUTION at the headline ({HEAD_SCOPE}, {RUNG_HEAD:g} bps, FULLMATCH),")
    P(f"      {len(HEADW)} rolling windows {HEADW.start.iloc[0].date()}..{HEADW.end.iloc[-1].date()}:")
    for o, n in HEADW.order.value_counts().items():
        tag = "  <- THE PUBLISHED ORDER" if o == " > ".join(PUBLISHED) else ""
        P(f"      {o:<28} {n:>4}  {n/len(HEADW):>6.1%}{tag}")
    P(f"      per-family win rate over the census: " + "  ".join(
        f"{f} median {HEADW[f'win_{f}'].median():.3f} "
        f"[{HEADW[f'win_{f}'].min():.3f}, {HEADW[f'win_{f}'].max():.3f}]" for f in FAMS))
    P(f"      full-sample reference at the same rung: " + "  ".join(
        f"{f} {float(s10[s10.family==f].win.mean()):.4f}" for f in FAMS))
    P(f"      windows in which QROLL's win rate is BELOW its own full-sample value: "
      f"{int((HEADW.win_QROLL < float(s10[s10.family=='QROLL'].win.mean())).sum())} of {len(HEADW)}")

    # ---------------- rule 8 on the claim ---------------------------------------------
    P(f"\n{'='*116}")
    P("D. PROTOCOL RULE 8 ON THE CLAIM - (L, step) chosen on the FIRST HALF of the census by")
    P("   share_exact alone, read ONCE on the SECOND HALF.  The IS/OOS boundary is the record's")
    P(f"   standing one ({IS_END} / {OOS_START}), applied to the window's END date.")
    P(f"{'='*116}")
    cut = pd.Timestamp(IS_END)
    r8 = []
    for L in LS:
        for st in STEPS:
            W = win_rates(L, st, RUNG_HEAD, "FULLMATCH", HEAD_SCOPE)
            iw, ow = W[W.end <= cut], W[W.end > cut]
            si, so = summarise(iw), summarise(ow)
            r8.append(dict(L=L, step=st, n_IS=si["n_win"], IS_exact=si["share_exact"],
                           n_OOS=so["n_win"], OOS_exact=so["share_exact"],
                           IS_top=si["share_top"], OOS_top=so["share_top"],
                           IS_modal=si["modal"], OOS_modal=so["modal"]))
    R8 = pd.DataFrame(r8)
    P(f"   {'L':>6} {'step':>5} {'n_IS':>5} {'IS exact':>9} {'n_OOS':>6} {'OOS exact':>10} "
      f"{'IS top':>7} {'OOS top':>8}  {'IS modal':<26} {'OOS modal':<26}")
    for _, r in R8.iterrows():
        P(f"   {r.L:>6.0f} {r.step:>5.0f} {r.n_IS:>5.0f} {r.IS_exact:>9.3f} {r.n_OOS:>6.0f} "
          f"{r.OOS_exact:>10.3f} {r.IS_top:>7.3f} {r.OOS_top:>8.3f}  {r.IS_modal:<26} "
          f"{r.OOS_modal:<26}")
    valid = R8[(R8.n_IS >= 3) & (R8.n_OOS >= 3)]
    pick = valid.loc[valid.IS_exact.idxmax()] if len(valid) else None
    if pick is not None:
        P(f"\n   IS pick: L = {pick.L:.0f}, step = {pick.step:.0f} (IS share_exact "
          f"{pick.IS_exact:.3f}) -> OOS share_exact read ONCE = {pick.OOS_exact:.3f}  "
          f"(|d| {abs(pick.OOS_exact-pick.IS_exact):.3f})")
    P(f"   Spearman(IS share_exact, OOS share_exact) over the {len(valid)} evaluable grid points: "
      f"{spearman(valid.IS_exact, valid.OOS_exact):.3f}")

    # ---------------- rule 8 on the books ---------------------------------------------
    P(f"\n{'='*116}")
    P("E. PROTOCOL RULE 8 ON THE BOOKS + BOTH KEEP PATHS (mandatory) - dial chosen on IS")
    P(f"   (..{IS_END}) by IS Sharpe alone, OOS ({OOS_START}..) read ONCE, against RULES v2 and SPY.")
    P(f"{'='*116}")
    for c in RUNGS:
        s = AR[AR.rung == c]
        w = WF[WF.rung == c]
        P(f"\n   cost rung {c:g} bps - {len(s)} arms, {len(w)} rule-8 picks")
        P(f"   {'panel':<6} {'family':<7} {'arms':>5} {'4a':>4} {'4b':>4} {'4b&twin4b':>10} "
          f"{'4b earned':>10} {'medOOSCAGR':>11} {'medOOSSh':>9} {'medOOSDD':>9}")
        for pn in ["U56", "B136", "SMALL"]:
            for f in FAMS:
                d = s[(s.panel == pn) & (s.family == f)]
                if d.empty:
                    continue
                earned = int((d.pass_4b & ~d.twin_pass_4b).sum())
                P(f"   {pn:<6} {f:<7} {len(d):>5} {int(d.pass_4a.sum()):>4} "
                  f"{int(d.pass_4b.sum()):>4} {int((d.pass_4b & d.twin_pass_4b).sum()):>10} "
                  f"{earned:>10} {d.OOS_CAGR.median():>11.2%} {d.OOS_Sharpe.median():>9.3f} "
                  f"{d.OOS_MaxDD.median():>9.2%}")
        P(f"   comparands: SPY OOS " + "  ".join(
            f"{pn} {float(s[s.panel==pn].SPY_OOS_CAGR.iloc[0]):.2%}/"
            f"{float(s[s.panel==pn].SPY_OOS_Sharpe.iloc[0]):.3f}/"
            f"{float(s[s.panel==pn].SPY_OOS_MaxDD.iloc[0]):.2%}" for pn in ["U56", "B136", "SMALL"]))
        P(f"   comparands: RULES v2 OOS " + "  ".join(
            f"{pn} {float(s[s.panel==pn].V2_OOS_CAGR.iloc[0]):.2%}/"
            f"{float(s[s.panel==pn].V2_OOS_Sharpe.iloc[0]):.3f}/"
            f"{float(s[s.panel==pn].V2_OOS_MaxDD.iloc[0]):.2%}" for pn in ["U56", "B136", "SMALL"]))
        P(f"   TOTALS  4a {int(s.pass_4a.sum())} of {len(s)};  4b {int(s.pass_4b.sum())};  "
          f"4b EARNED (own twin fails 4b) {int((s.pass_4b & ~s.twin_pass_4b).sum())};  "
          f"rule-8 picks 4a {int(w.pass_4a.sum())} of {len(w)}, 4b {int(w.pass_4b.sum())}")
    hs = AR[AR.rung == RUNG_HEAD]
    best = hs[hs.pass_4b & ~hs.twin_pass_4b].sort_values("OOS_Sharpe", ascending=False)
    P(f"\n   EARNED 4b passers at {RUNG_HEAD:g} bps (own matched-gross twin FAILS 4b), top 8 by OOS Sharpe:")
    if best.empty:
        P("      none.")
    for _, r in best.head(8).iterrows():
        P(f"      {r.panel:<6} {r.arm:<28} {r.CAGR:>7.2%}/{r.Sharpe:>6.3f}/{r.MaxDD:>7.2%}  "
          f"H {r.H1:.3f}/{r.H2:.3f}  OOS {r.OOS_CAGR:>7.2%}/{r.OOS_Sharpe:>6.3f}/{r.OOS_MaxDD:>7.2%}"
          f"  twin Sh {r.twin_Sharpe:.3f}")

    # ---------------- hypotheses ------------------------------------------------------
    def gsel(**kw):
        d = GRD
        for k, v in kw.items():
            d = d[d[k] == v]
        return d.iloc[0] if len(d) else None

    head = gsel(L=L_HEAD, step=STEP_HEAD, rung=RUNG_HEAD, conv="FULLMATCH", scope=HEAD_SCOPE)
    lcol = [float(gsel(L=L, step=STEP_HEAD, rung=RUNG_HEAD, conv="FULLMATCH",
                       scope=HEAD_SCOPE).share_exact) for L in LS]
    steprange = {L: (max(float(gsel(L=L, step=st, rung=RUNG_HEAD, conv="FULLMATCH",
                                    scope=HEAD_SCOPE).share_exact) for st in STEPS)
                     - min(float(gsel(L=L, step=st, rung=RUNG_HEAD, conv="FULLMATCH",
                                      scope=HEAD_SCOPE).share_exact) for st in STEPS)) for L in LS}
    c0 = float(gsel(L=L_HEAD, step=STEP_HEAD, rung=0.0, conv="FULLMATCH", scope=HEAD_SCOPE).share_exact)
    c25 = float(gsel(L=L_HEAD, step=STEP_HEAD, rung=25.0, conv="FULLMATCH", scope=HEAD_SCOPE).share_exact)
    wm = float(gsel(L=L_HEAD, step=STEP_HEAD, rung=RUNG_HEAD, conv="WINMATCH", scope=HEAD_SCOPE).share_exact)
    pans = [float(gsel(L=L_HEAD, step=STEP_HEAD, rung=RUNG_HEAD, conv="FULLMATCH",
                       scope=p).share_exact) for p in ["U56", "B136", "SMALL"]]
    rho_L = spearman(LS, lcol)

    H = [("H_REPRO   the full-sample reading reproduces idea 605's committed ordering (G4/G5)", bool(g4 and g5)),
         (f"H_MAJORITY {' > '.join(PUBLISHED)} is the MODAL rolling order at the headline",
          bool(head.modal == " > ".join(PUBLISHED))),
         ("H_HALF    share_exact > 0.50 at the headline [the queue's literal question]",
          bool(head.share_exact > 0.50)),
         ("H_TOP     share_top > 0.80 at the headline (QROLL on top, the strong leg alone)",
          bool(head.share_top > 0.80)),
         ("H_NOINV   share_reverse < 0.10 at the headline", bool(head.share_reverse < 0.10)),
         ("H_LMONO   share_exact rises with L: Spearman over the five L rungs >= +0.80",
          bool(np.isfinite(rho_L) and rho_L >= 0.80)),
         ("H_STEPFREE at every L, max-min of share_exact across the four steps <= 0.05",
          bool(all(v <= 0.05 for v in steprange.values()))),
         ("H_COSTINV |share_exact(0) - (10)| <= 0.10 and |share_exact(25) - (10)| <= 0.10",
          bool(abs(c0 - head.share_exact) <= 0.10 and abs(c25 - head.share_exact) <= 0.10)),
         ("H_MATCH   |share_exact(FULLMATCH) - share_exact(WINMATCH)| <= 0.10",
          bool(abs(wm - head.share_exact) <= 0.10)),
         ("H_PANEL   the three panels' headline share_exact lie within 0.20 of each other",
          bool(max(pans) - min(pans) <= 0.20)),
         ("H_R8CLAIM the IS-picked (L, step) reproduces its share within 0.10 on OOS, read once",
          (bool(abs(pick.OOS_exact - pick.IS_exact) <= 0.10) if pick is not None else None))]

    P(f"\n{'='*116}")
    P("PRE-REGISTERED HYPOTHESES")
    P(f"{'='*116}")
    P(f"   headline cell: L={L_HEAD}, step={STEP_HEAD}, {RUNG_HEAD:g} bps, FULLMATCH, {HEAD_SCOPE} - "
      f"{int(head.n_win)} windows, share_exact {head.share_exact:.3f}, share_top {head.share_top:.3f},")
    P(f"   share_bottom {head.share_bottom:.3f}, share_reverse {head.share_reverse:.3f}, "
      f"tied {head.share_tied:.3f}, median rho {head.med_rho:.3f}, modal '{head.modal}' "
      f"({head.modal_share:.3f}).")
    P(f"   share_exact by L at step {STEP_HEAD}: " +
      "  ".join(f"{L}:{v:.3f}" for L, v in zip(LS, lcol)) + f"   Spearman {rho_L:.3f}")
    P(f"   step range by L: " + "  ".join(f"{L}:{v:.3f}" for L, v in steprange.items()))
    P(f"   cost: 0bps {c0:.3f}  10bps {head.share_exact:.3f}  25bps {c25:.3f};  "
      f"WINMATCH {wm:.3f};  panels U56 {pans[0]:.3f} B136 {pans[1]:.3f} SMALL {pans[2]:.3f}")
    h3 = gsel(L=L_HEAD, step=STEP_HEAD, rung=RUNG_HEAD, conv="FULLMATCH", scope=OTHER_SCOPE)
    l3 = [float(gsel(L=L, step=STEP_HEAD, rung=RUNG_HEAD, conv="FULLMATCH",
                     scope=OTHER_SCOPE).share_exact) for L in LS]
    P(f"\n   THE SAME CELL ON {OTHER_SCOPE}, printed beside {HEAD_SCOPE} so the gate's choice")
    P(f"   of scope is auditable rather than a silent selection:")
    P(f"      {int(h3.n_win)} windows, share_exact {h3.share_exact:.3f}, share_top {h3.share_top:.3f}, "
      f"share_bottom {h3.share_bottom:.3f}, share_reverse {h3.share_reverse:.3f}, "
      f"tied {h3.share_tied:.3f}, median rho {h3.med_rho:.3f}, modal '{h3.modal}'")
    P(f"      share_exact by L: " + "  ".join(f"{L}:{v:.3f}" for L, v in zip(LS, l3))
      + f"   Spearman {spearman(LS, l3):.3f}")
    P(f"      the four scope-dependent hypotheses re-read on {OTHER_SCOPE}: "
      f"H_MAJORITY {'PASS' if h3.modal == ' > '.join(PUBLISHED) else 'FAIL'}, "
      f"H_HALF {'PASS' if h3.share_exact > 0.50 else 'FAIL'}, "
      f"H_TOP {'PASS' if h3.share_top > 0.80 else 'FAIL'}, "
      f"H_NOINV {'PASS' if h3.share_reverse < 0.10 else 'FAIL'}")
    for nm, v in H:
        P(f"   {nm:<76} {'N/A' if v is None else ('PASS' if v else 'FAIL')}")
    ev = [v for _, v in H if v is not None]
    P(f"\n   {sum(bool(v) for v in ev)} of {len(ev)} EVALUABLE pre-registered hypotheses pass"
      f" (read on {HEAD_SCOPE}; the {OTHER_SCOPE} re-reading is printed above).")

    P(f"\n   THE ANSWER the queue asked for: on a rolling {L_HEAD}-day ({L_HEAD/252:.0f}-year) census")
    P(f"   stepped {STEP_HEAD} days, the published full-sample order {' > '.join(PUBLISHED)} is the")
    P(f"   one a reader would have seen in {head.share_exact:.1%} of windows "
      f"({int(head.share_exact*head.n_win)} of {int(head.n_win)}); its strong leg alone (QROLL on")
    P(f"   top) in {head.share_top:.1%}; the exact inversion in {head.share_reverse:.1%}.")
    P(f"\nRUNTIME {time.time()-T_START:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(AR=AR, WF=WF, GRD=GRD, R8=R8, HEADW=HEADW, H=H)


if __name__ == "__main__":
    main()

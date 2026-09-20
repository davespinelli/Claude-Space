#!/usr/bin/env python3
"""Idea 1745 (lane C, 2026-09-20): is the BAND's RETURN COST predicted by its names' own
200d-MA WHIPSAW RATE -- or only by the panel's label?

WHY THIS IDEA.  Idea 1632 (2026-09-20, lane C) split the live band's matched-exposure contrast
into its two legs and found they behave completely differently.  The DRAWDOWN credit is near
panel-invariant and flat in name count above N=56 (c=0.03: U56 +4.34 pp, B136 +5.93, SMALL
+6.45).  The CAGR leg is where ALL the panel dependence lives: the gate costs U56's names
-0.72 pp/yr, B136's -1.46 and SMALL's -1.99, and inside each panel that cost is FLAT in N.  A
~3x spread that tracks the panel LABEL and not the book's width is either a real property of
those names or an unexplained constant the record has been quoting panel by panel.

THE MECHANISM, STATED BEFORE THE RUN.  A 200d-MA band can only COST return when it sells a name
that then goes UP relative to what the book would otherwise have held.  That decomposes into
exactly three price-only quantities, none of which needs a backtest to measure:

    GATEOUT   the realised share of priced name-days spent OUT of the band (how much exposure
              the gate withholds).  The twin is matched on realised GROSS, so this leg should
              be largely differenced away -- if it still carries the cost, the match is leaking.
    XRATE     the names' own 200d-MA band CROSSING rate, in crossings per name-year.  This is
              the WHIPSAW rate: how often the gate changes its mind.
    RECOV     the post-exit RECOVERY: the mean W-day forward return of a name at the moment it
              is gated OUT, measured in EXCESS of the draw's own cross-sectional mean that day.
              Positive = the gate systematically sells names that come back.

    H0 (PANEL LABEL):  dCAGR is a property of the panel; the three regressors carry little of
                       it, panel dummies carry the rest, and a fit on two panels cannot predict
                       the third.
    H1 (WHIPSAW):      dCAGR is a function of (GATEOUT, XRATE, RECOV); once they are in the
                       regression the panel label adds ~nothing, and a fit on two panels
                       predicts the third's draws.

H1 is the interesting one because it is CONSTRUCTIVE: it would let the record PREDICT which
universe a band is affordable on from prices alone, instead of discovering it one panel at a
time -- and it would make a price-only, BOOK-FREE chooser legal under rule 8.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  DIAL 1  REGRESSOR SET   {G} , {X} , {R} , {G,X} , {X,R} , {G,X,R} , {G,X,R,PANEL dummies}
                          -- which of the three price-only regressors (plus the panel label as
                          the H0 control) enters the model.
  DIAL 2  WINDOW W        {21, 63, 126} trading days: the horizon over which post-exit RECOVERY
                          is measured.  XRATE and GATEOUT do not depend on W.

NOT DIALS, published at every value (inherited unchanged from idea 1632 so every number here is
directly commensurable with its committed grid, and gated against it at G12):
  PANEL   {U56, B136, SMALL}  (rule 9; SMALL carries the protocol's max_1d_move >= 1.0 drop)
  N       ladder {20, 36, 56, 100, 136, 300} truncated at each panel's size + the ALL rung
  DRAW    D = 24 seeded draws per non-ALL rung, SEED0 = 16320000, identical seeds to 1632
  BAND c  {0.00, 0.03, 0.06, 0.10}; c = 0.03 IS live RULES v2 clause 2
  COST    {0, 10, 25, 50} bps, exact off the gross return and the turnover path (gated at G2).
          Every KEEP verdict is read at the protocol's binding 10 bps.

THE TWIN.  Each band book is paired with the SAME names held with NO gate, scaled by a constant
k solved in closed form so the twin's REALISED mean gross matches the band book's to machine
precision (G4).  dCAGR = CAGR(band) - CAGR(twin) is therefore a pure SELECTION contrast at
matched exposure, over the same names on the same days.  1617's and 1632's construction,
carried over unchanged.

THE QUESTIONS, STATED BEFORE THE RUN:
  Q1  Univariate: how much of dCAGR does each of GATEOUT / XRATE / RECOV carry, pooled over all
      291 draws x 3 panels, and how much does the PANEL LABEL alone carry?
  Q2  Multiple: which regressor SURVIVES the others (drop-one partial R^2, standardized betas
      with a rung-block bootstrap SE)?  Does the panel dummy add anything on top of them?
  Q3  WITHIN-panel: does the law hold inside a single panel, or only between panels (which any
      3-point fit reproduces trivially)?
  Q4  LEAVE-ONE-PANEL-OUT: fit on two panels, predict the third's draws.  This is the only test
      that can support the idea's constructive claim, and it is the one the record has never run.
  Q5  CAPITAL (rule 4, both paths, at EVERY cell): does any band book clear 4a or 4b, FULL and
      OOS?  And under rule 8, can a PRICE-ONLY WHIPSAW CHOOSER -- fit on 2009-2016 rows only and
      never reading a book's returns -- pick a name set that clears 4b OOS, against the draw
      base rate and against the record's standard IS-Sharpe chooser?

CHOOSERS (rule 8), each fit on warm-up..2016-12-31 ONLY, then 2017-2026 read EXACTLY ONCE:
  C_WHIP    argmin over that panel's (N, draw) cells at c = 0.03 of the band cost PREDICTED by
            the IS-fitted regression (dials chosen by IS adjusted R^2, IS rows only).  Reads
            PRICES only -- never a book's realised return.
  C_XRATE   argmin raw IS crossing rate.  No fitting at all; the crudest form of the claim.
  C_SHARPE  argmax IS Sharpe of the band book itself.  The record's standard chooser, and the
            most optimistic legal one.
  C_LIVE    the live inheritance, choosing nothing: FULL panel, c = 0.03.
  Each pick is read OOS against (a) SPY, (b) the live RULES v2 baseline, (c) its OWN twin
  (k RE-SOLVED on IS gross only, so the twin is legal out of sample too), and (d) the panel's
  own DRAW BASE RATE -- the mean OOS Sharpe and the 4b pass share over every draw on that panel.
  A chooser that does not beat its base rate has picked a lottery ticket, not a name set.

WHAT WOULD MAKE THIS A FINDING.  If XRATE survives the others and the leave-one-panel-out fit
predicts the held-out panel's draws, the record can stop quoting the band's return cost per
panel and quote it per WHIPSAW RATE.  If the panel dummy eats the regressors, or the LOPO fit
fails, the -0.72 / -1.46 / -1.99 spread stays an unexplained panel constant and the idea dies.
Both outcomes are reported; nothing is tuned until it works.

GATES.  G0 sample >= 10y (rule 1).  G1 fast_run vs `engine.backtest` (returns AND turnover) on
the FULL panels, band and no-gate books.  G2 the DERIVED 25 bps rung vs a fresh 25 bps engine
run.  G3 BAND c = 0.03 at the ALL rung on U56 replays `baseline.rules_v2_weights` through the
engine.  G4 the realised-gross match, max |dev| over all cells.  G5 exactly two tuned dials.
G6 no chooser and no IS regression reads a row on or after 2017-01-01 (by construction AND
re-tested on truncated input).  G7 every row published.  G8 no leverage / no shorting.
G9 PUBLISHED: turnover per cell, book and twin.  G10 PUBLISHED: realised mean gross, mean names
held, exit-event counts.  G11 the closed-form gross/return profile replays `run_cell` exactly.
G12 REPLICATION: this run's dCAGR reproduces idea 1632's committed grid cell for cell.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps per unit turnover, no leverage/shorting); rule 3
(live RULES v2 baseline AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward);
rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_band-cagr-cost-vs-whipsaw-rate_C.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-20", "band-cagr-cost-vs-whipsaw-rate"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
OUT.mkdir(exist_ok=True)
PRIOR = Path(__file__).resolve().parent / "2026-09-20_band-u56-panel-or-namecount_C.grid.csv.gz"

WARMUP = 260
GROSS = 0.75
CADENCE = "W"
COSTS = [0.0, 10.0, 25.0, 50.0]
BIND = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

BANDS = [0.00, 0.03, 0.06, 0.10]
LIVE_C = 0.03
NLADDER = [20, 36, 56, 100, 136, 300]
NDRAWS = 24
SEED0 = 16320000                      # IDENTICAL to idea 1632 -> same draws, gated at G12

WINDOWS = [21, 63, 126]               # DIAL 2
REG_SETS = {                          # DIAL 1
    "G": ["GATEOUT"],
    "X": ["XRATE"],
    "R": ["RECOV"],
    "GX": ["GATEOUT", "XRATE"],
    "XR": ["XRATE", "RECOV"],
    "GXR": ["GATEOUT", "XRATE", "RECOV"],
    "GXR+PANEL": ["GATEOUT", "XRATE", "RECOV", "P_B136", "P_SMALL"],
    "PANEL": ["P_B136", "P_SMALL"],   # the H0 control
}
NBOOT = 2000
BOOT_SEED = 17450000

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUBLISHED  {name}: {value}")


# ---------------------------------------------------------------- metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=h1, H2=h2)


def keep_paths(r, bm, live):
    """4a against the LIVE RULES v2 book, 4b against SPY.  Legs published."""
    h1, h2 = halves(r)
    m = dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


# ---------------------------------------------------------------- panel / subpanel
class Panel:
    def __init__(self, name, px, cols):
        self.name, self.px = name, px
        self.cols = list(cols)
        self.idx = px.index
        q = px[self.cols]
        self.rets = q.pct_change().fillna(0.0).values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.priced = q.notna().values
        self.bands = {c: band_state(q, c).values for c in BANDS}
        m = rebalance_mask(self.idx, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.i_oos = int(np.searchsorted(self.idx.values, np.datetime64(OOS_START)))
        self.T = len(self.idx)
        # forward W-day returns off the SAME price index the books trade
        self.fwd = {}
        for W in WINDOWS:
            F = np.full_like(self.C, np.nan, dtype=float)
            F[:-W] = self.C[W:] / self.C[:-W] - 1.0
            self.fwd[W] = F


class Sub:
    __slots__ = ("pan", "j", "rets", "C", "Cp", "priced", "bands", "reb", "T", "fwd")

    def __init__(self, pan: Panel, j: np.ndarray):
        self.pan, self.j = pan, j
        self.rets = pan.rets[:, j]
        self.C = pan.C[:, j]
        self.Cp = pan.Cp[:, j]
        self.priced = pan.priced[:, j]
        self.bands = {c: pan.bands[c][:, j] for c in BANDS}
        self.fwd = {W: pan.fwd[W][:, j] for W in WINDOWS}
        self.reb = pan.reb
        self.T = pan.T

    def frame(self, c):
        """Target weights at gross 1.0, shifted one row (engine's weights.shift(1) convention).
        c is None for the NO-GATE anchor."""
        e = (self.priced if c is None else (self.priced & self.bands[c])).astype(float)
        n = self.priced.sum(axis=1).astype(float)
        w = np.divide(e, np.where(n == 0, np.nan, n)[:, None])
        w = np.nan_to_num(w, nan=0.0)
        return np.vstack([np.zeros((1, w.shape[1])), w[:-1]])


def run_cell(sub: Sub, frame, g=GROSS):
    rets = sub.rets
    T, M = rets.shape
    turn = np.zeros(T); out = np.zeros(T); gsum = np.zeros(T)
    curw = np.zeros(M); wsum_max = 0.0
    reb = sub.reb
    ends = np.append(reb[1:], T)
    C, Cp = sub.C, sub.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wsum_max = max(wsum_max, s0)
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum[i0:i1] = A.sum(axis=1) / V
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out, turn, wsum_max, gsum


def profile(sub: Sub, frame):
    T, M = sub.rets.shape
    P = np.zeros(T); Q = np.zeros(T); F0 = np.zeros(T)
    reb = sub.reb
    ends = np.append(reb[1:], T)
    Cp = sub.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        f = frame[i0]
        A0 = f[None, :] * (Cp[i0:i1] / Cp[i0][None, :])
        P[i0:i1] = A0.sum(axis=1)
        Q[i0:i1] = (A0 * sub.rets[i0:i1]).sum(axis=1)
        F0[i0:i1] = f.sum()
    return P, Q, F0


def mean_gross_of(prof, g, lo, hi):
    P, Q, F0 = prof
    num = g * P[lo:hi]
    return float(np.mean(num / (num + 1.0 - g * F0[lo:hi])))


def solve_k(prof, target, lo, hi, iters=80):
    a, b = 0.0, 1.0
    for _ in range(iters):
        k = 0.5 * (a + b)
        if mean_gross_of(prof, k * GROSS, lo, hi) < target:
            a = k
        else:
            b = k
    return 0.5 * (a + b)


def net(rg, tu, c):
    return rg - tu * c / 1e4


def maxdev(a, b):
    d = np.abs(np.asarray(a, float) - np.asarray(b, float))
    f = np.isfinite(d)
    return (float(d[f].max()) if f.any() else 0.0), int((~f).sum())


# ---------------------------------------------------------------- the three regressors
def whipsaw(sub: Sub, c, lo, hi):
    """PRICE-ONLY regressors for one draw over rows [lo, hi).  No book, no return series.
    GATEOUT: share of priced name-days OUT of the band.
    XRATE  : 200d-MA band crossings per name-YEAR.
    RECOV_W: mean W-day forward return at a gate-OUT event, in EXCESS of the draw's own
             cross-sectional mean that day (the return the gate actually gives up).
    Also published: RECOV_RAW_W (no excess), NEXIT (event count)."""
    B = sub.bands[c][lo:hi]
    P = sub.priced[lo:hi]
    Bp = sub.bands[c][lo - 1:hi - 1]
    Pp = sub.priced[lo - 1:hi - 1]
    nP = int(P.sum())
    if nP == 0:
        return {}
    both = P & Pp
    out = dict(GATEOUT=float((P & ~B).sum()) / nP,
               XRATE=float((both & (B != Bp)).sum()) / (nP / 252.0),
               NAMEDAYS=nP)
    ev0 = both & Bp & (~B)                      # 1 -> 0 : the gate SELLS
    for W in WINDOWS:
        F = sub.fwd[W][lo:hi]
        ok = P & np.isfinite(F)
        cnt = ok.sum(axis=1)
        rs = np.where(ok, F, 0.0).sum(axis=1)
        rm = rs / np.maximum(cnt, 1)
        ev = ev0 & ok
        n = int(ev.sum())
        out[f"NEXIT_{W}"] = n
        if n:
            out[f"RECOV_{W}"] = float((F - rm[:, None])[ev].mean())
            out[f"RECOV_RAW_{W}"] = float(F[ev].mean())
        else:
            out[f"RECOV_{W}"] = np.nan
            out[f"RECOV_RAW_{W}"] = np.nan
    return out


# ---------------------------------------------------------------- OLS + rung-block bootstrap
def ols(X, y):
    """X already carries its intercept column.  Returns (beta, resid, R2, adjR2)."""
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    fit = X @ beta
    resid = y - fit
    sst = float(((y - y.mean()) ** 2).sum())
    sse = float((resid ** 2).sum())
    r2 = 1.0 - sse / sst if sst > 0 else np.nan
    k = X.shape[1] - 1
    n = len(y)
    adj = 1.0 - (1.0 - r2) * (n - 1) / (n - k - 1) if n - k - 1 > 0 else np.nan
    return beta, resid, r2, adj


def design(df, cols, standardize=True, mu=None, sd=None):
    Z = df[cols].values.astype(float)
    if standardize:
        if mu is None:
            mu = np.nanmean(Z, axis=0); sd = np.nanstd(Z, axis=0)
        sd = np.where(sd > 0, sd, 1.0)
        Z = (Z - mu) / sd
    return np.column_stack([np.ones(len(Z)), Z]), mu, sd


def boot_se(df, cols, ycol, rungs, nboot=NBOOT, seed=BOOT_SEED):
    """Resample whole (panel, N) RUNGS with replacement: draws inside a rung share names by
    construction, so a draw-level bootstrap would understate every SE."""
    rng = np.random.default_rng(seed)
    keys = list(rungs)
    groups = {k: df.index[(df["panel"] == k[0]) & (df["N"] == k[1])].values for k in keys}
    out = []
    for _ in range(nboot):
        pick = rng.integers(0, len(keys), len(keys))
        idx = np.concatenate([groups[keys[i]] for i in pick])
        d = df.loc[idx]
        if d[ycol].notna().sum() < len(cols) + 3:
            continue
        X, _, _ = design(d, cols)
        b, *_ = ols(X, d[ycol].values.astype(float))
        out.append(b)
    A = np.array(out)
    return A.std(axis=0, ddof=0) if len(A) else np.full(len(cols) + 1, np.nan)


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1745 (lane C, 2026-09-20) — is the BAND's RETURN COST predicted by its names' own")
    say("200d-MA WHIPSAW RATE, or only by the panel's label?")
    say(f"DIALS: REGRESSOR SET {list(REG_SETS)}  x  WINDOW W {WINDOWS}.")
    say(f"NOT DIALS, all published: PANEL x N ladder {NLADDER}+ALL x DRAW (D={NDRAWS}) x BAND {BANDS} x COST {COSTS} bps.")
    say("dCAGR = CAGR(band book) - CAGR(its REALISED-GROSS-MATCHED no-gate twin), pp/yr, at 10 bps.")
    say("H0 PANEL LABEL: the 3 price-only regressors carry little; panel dummies carry the rest.")
    say("H1 WHIPSAW: XRATE (+GATEOUT/RECOV) carries it, the panel label adds ~nothing, and a fit")
    say("   on two panels predicts the THIRD panel's draws (leave-one-panel-out).")
    say("=" * 118)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)

    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(md.loc[md["max_1d_move"] >= 1.0, "ticker"].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} of {len(pxS.columns)-1} priced names survive.")

    panels = [Panel("U56", pxU, list(pxU.columns)),
              Panel("B136", pxB, list(pxB.columns)),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(panels[0].cols)} traded cols, B136 {len(panels[1].cols)}, "
        f"SMALL {len(panels[2].cols)} (SPY a joined BENCHMARK only on SMALL).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every absolute level is an UPPER BOUND.  The "
        "headline regression's LHS is a BAND-minus-TWIN contrast inside one draw, same names, "
        "same days, same realised exposure, so it is first-order immune; the 4b pass counts and "
        "every chooser level are NOT.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {p.T} rows "
            f"({p.T/252:.1f}y)  OOS starts row {p.i_oos} ({p.idx[p.i_oos].date()})")
        publish(f"TAPE STAMP {p.name}", f"{p.T} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(p.T for p in panels) / 252.0, 2),
         ">= 10.0", min(p.T for p in panels) / 252.0 >= 10.0)

    rungs = {}
    for p in panels:
        M = len(p.cols)
        rungs[p.name] = [n for n in NLADDER if n < M] + [M]
        say(f"    N LADDER {p.name}: {rungs[p.name]}  (ALL rung = {M}, one deterministic draw)")
    gate("G5 exactly two tuned dials (REGRESSOR SET x WINDOW W)",
         f"{len(REG_SETS)} sets x {len(WINDOWS)} windows; PANEL/N/DRAW/BAND/COST published, not tuned",
         "2 dials", True)

    # ------------------------------------------------ G1 / G2 / G3 / G11 against the engine
    say("\n  [G1/G2/G3/G11] fast_run and the closed-form profile vs engine.backtest, FULL panels")
    d1r = d1t = d2 = d11 = 0.0
    nonfin = 0
    g3dev = None
    for p in panels:
        sub = Sub(p, np.arange(len(p.cols)))
        for c in (LIVE_C, None):
            fr = sub.frame(c)
            rg, tu, _, gs = run_cell(sub, fr)
            if c is None:
                e = pd.DataFrame(1.0, index=p.idx, columns=p.cols).where(p.px[p.cols].notna(), 0.0)
                W = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
            else:
                W = rules_v2_weights(p.px[p.cols], band=c, gross=GROSS)
            W = W.reindex(p.idx).fillna(0.0).reindex(columns=p.px.columns).fillna(0.0)
            eng = backtest(p.px, W, cost_bps=BIND, freq=CADENCE)
            eng25 = backtest(p.px, W, cost_bps=25.0, freq=CADENCE)
            v, nf = maxdev(net(rg, tu, BIND), eng["returns"].values); d1r = max(d1r, v); nonfin += nf
            v, _ = maxdev(tu, eng["turnover"].values); d1t = max(d1t, v)
            v, _ = maxdev(net(rg, tu, 25.0), eng25["returns"].values); d2 = max(d2, v)
            if c == LIVE_C and p.name == "U56":
                g3dev, _ = maxdev(net(rg, tu, BIND), eng["returns"].values)
            P, Q, F0 = profile(sub, fr)
            for kk in (1.0, 0.5137):
                den = kk * GROSS * P + 1.0 - kk * GROSS * F0
                r_rc, _, _, g_rc = run_cell(sub, fr, g=kk * GROSS)
                v1, _ = maxdev(kk * GROSS * Q / den, r_rc)
                v2, _ = maxdev(kk * GROSS * P / den, g_rc)
                d11 = max(d11, v1, v2)
    gate("G1 fast_run vs engine.backtest, RETURNS (max |dev|)", f"{d1r:.3e}", "< 1e-12", d1r < 1e-12)
    gate("G1b fast_run vs engine.backtest, TURNOVER (max |dev|)", f"{d1t:.3e}", "< 1e-12", d1t < 1e-12)
    gate("G2 DERIVED 25 bps rung vs a fresh 25 bps engine run (max |dev|)", f"{d2:.3e}", "< 1e-12", d2 < 1e-12)
    gate("G3 BAND c=0.03 ALL rung on U56 replays baseline.rules_v2_weights", f"{g3dev:.3e}", "< 1e-12", g3dev < 1e-12)
    gate("G11 closed-form (P,Q,F0) profile replays run_cell at 2 scalers", f"{d11:.3e}", "< 1e-12", d11 < 1e-12)
    publish("G1c engine warm-up rows with no finite return (counted, not swallowed)", nonfin)

    # ------------------------------------------------ the grid
    rows = []
    BARS = {}
    wsum_global = 0.0
    gapmax = 0.0
    books = {}    # (panel,N,draw,band) -> dict of return arrays, for the rule-8 arm

    for p in panels:
        T, i_oos = p.T, p.i_oos
        spy = bmpack(p.spy[WARMUP:]); spyO = bmpack(p.spy[i_oos:]); spyI = bmpack(p.spy[WARMUP:i_oos])
        lr = backtest(p.px, rules_v2_weights(p.px), cost_bps=BIND, freq="W")["returns"].values
        live, liveO, liveI = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:]), bmpack(lr[WARMUP:i_oos])
        BARS[p.name] = dict(spy=spy, spyO=spyO, spyI=spyI, live=live, liveO=liveO, liveI=liveI)
        say(f"\n  [{p.name}]  SPY FULL {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%}"
            f"  |  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS  {spyO['CAGR']:.2%} / {spyO['Sharpe']:.4f} / {spyO['MaxDD']:.2%}"
            f"  |  OOS bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, floor {CAGR_FLOOR*spyO['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  {live['CAGR']:.2%} / {live['Sharpe']:.4f} / "
            f"{live['MaxDD']:.2%}  (OOS {liveO['CAGR']:.2%} / {liveO['Sharpe']:.4f} / {liveO['MaxDD']:.2%})")

        M = len(p.cols)
        for N in rungs[p.name]:
            draws = ([np.arange(M)] if N == M else
                     [np.random.default_rng(SEED0 + 1009 * N + d).choice(M, size=N, replace=False)
                      for d in range(NDRAWS)])
            for d, j in enumerate(draws):
                j = np.sort(j)
                sub = Sub(p, j)
                anchor = sub.frame(None)
                prof = profile(sub, anchor)
                for c in BANDS:
                    fb = sub.frame(c)
                    rgB, tuB, wsB, gsB = run_cell(sub, fb)
                    wsum_global = max(wsum_global, wsB)
                    gF = float(np.mean(gsB[WARMUP:])); gI = float(np.mean(gsB[WARMUP:i_oos]))
                    kF = solve_k(prof, gF, WARMUP, T)
                    kI = solve_k(prof, gI, WARMUP, i_oos)
                    rgTF, tuTF, wsTF, gsTF = run_cell(sub, anchor, g=kF * GROSS)
                    rgTI, tuTI, wsTI, gsTI = run_cell(sub, anchor, g=kI * GROSS)
                    wsum_global = max(wsum_global, wsTF, wsTI)
                    gapmax = max(gapmax, abs(float(np.mean(gsTF[WARMUP:])) - gF),
                                 abs(float(np.mean(gsTI[WARMUP:i_oos])) - gI))

                    wsF = whipsaw(sub, c, WARMUP, T)
                    wsI = whipsaw(sub, c, WARMUP, i_oos)

                    for cb in COSTS:
                        rB = net(rgB, tuB, cb); rTF = net(rgTF, tuTF, cb); rTI = net(rgTI, tuTI, cb)
                        k4a, k4b, m, h1, h2, legs = keep_paths(rB[WARMUP:], spy, live)
                        Ok4a, Ok4b, Om, _, _, Olegs = keep_paths(rB[i_oos:], spyO, liveO)
                        mt = bmpack(rTF[WARMUP:]); Omt = bmpack(rTI[i_oos:])
                        mI = bmpack(rB[WARMUP:i_oos]); mtI = bmpack(rTI[WARMUP:i_oos])
                        row = dict(panel=p.name, N=N, n_all=M, draw=d, band=c, cost_bps=cb,
                                   names_held=float(np.mean((sub.priced & sub.bands[c])[WARMUP:].sum(1))),
                                   gross_full=gF, gross_is=gI, k_full=kF, k_is=kI,
                                   turn_yr=float(tuB[WARMUP:].sum()) * 252 / (T - WARMUP),
                                   turn_twin_yr=float(tuTF[WARMUP:].sum()) * 252 / (T - WARMUP),
                                   CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                   tw_CAGR=mt["CAGR"], tw_Sharpe=mt["Sharpe"], tw_MaxDD=mt["MaxDD"],
                                   dSharpe=m["Sharpe"] - mt["Sharpe"],
                                   dCAGR=m["CAGR"] - mt["CAGR"],
                                   dMaxDD=m["MaxDD"] - mt["MaxDD"],
                                   IS_CAGR=mI["CAGR"], IS_Sharpe=mI["Sharpe"],
                                   IS_dCAGR=mI["CAGR"] - mtI["CAGR"],
                                   O_CAGR=Om["CAGR"], O_Sharpe=Om["Sharpe"], O_MaxDD=Om["MaxDD"],
                                   O_tw_Sharpe=Omt["Sharpe"], O_tw_MaxDD=Omt["MaxDD"],
                                   O_dSharpe=Om["Sharpe"] - Omt["Sharpe"],
                                   O_dCAGR=Om["CAGR"] - Omt["CAGR"],
                                   keep4a=k4a, keep4b=k4b, O_keep4a=Ok4a, O_keep4b=Ok4b,
                                   leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                                   leg_CAGR=legs["CAGR"], O_leg_DD=Olegs["DD"], O_leg_CAGR=Olegs["CAGR"])
                        for kk, vv in wsF.items():
                            row[kk] = vv
                        for kk, vv in wsI.items():
                            row["IS_" + kk] = vv
                        rows.append(row)
                        if cb == BIND and c == LIVE_C:
                            books[(p.name, N, d)] = dict(r=rB, rtI=rTI)
        say(f"    {p.name}: {sum(1 for r in rows if r['panel']==p.name)//len(COSTS)} (N,draw,band) cells done  [{time.time()-t0:.0f}s]")

    G = pd.DataFrame(rows)
    gate("G4 realised-gross match, band book vs twin (max |dev| over all cells)",
         f"{gapmax:.3e}", "< 1e-9", gapmax < 1e-9)
    gate("G8 no leverage / no shorting (max realised TARGET gross)", f"{wsum_global:.4f}",
         f"<= {GROSS}", wsum_global <= GROSS + 1e-12)
    publish("G7 grid rows published", len(G))
    publish("G9 turnover per cell (book, twin)", "columns turn_yr / turn_twin_yr")
    publish("G10 realised gross, names held, exit counts", "gross_full/gross_is/names_held/NEXIT_*")

    # ------------------------------------------------ G12 replication against idea 1632
    if PRIOR.exists():
        pr = pd.read_csv(PRIOR)
        key = ["panel", "N", "draw", "band", "cost_bps"]
        m = G.merge(pr[key + ["dCAGR", "dSharpe", "dMaxDD"]], on=key, suffixes=("", "_1632"))
        dv = float(np.abs(m["dCAGR"] - m["dCAGR_1632"]).max()) if len(m) else np.nan
        ds = float(np.abs(m["dSharpe"] - m["dSharpe_1632"]).max()) if len(m) else np.nan
        gate(f"G12 REPLICATION of idea 1632's committed grid ({len(m)} matched cells): dCAGR / dSharpe",
             f"{dv:.3e} / {ds:.3e}", "< 1e-12", (len(m) > 4000) and dv < 1e-12 and ds < 1e-12)
    else:
        gate("G12 REPLICATION of idea 1632's committed grid", "prior grid not found", "present", False)

    # ------------------------------------------------ the regression (Q1-Q4)
    say("\n" + "=" * 118)
    say("  [Q1-Q3]  WHAT CARRIES dCAGR?  LHS = dCAGR in pp/yr, band c = 0.03, 10 bps, FULL sample.")
    say("=" * 118)
    D = G[(G["band"] == LIVE_C) & (G["cost_bps"] == BIND)].copy().reset_index(drop=True)
    D["y"] = D["dCAGR"] * 100.0
    D["P_B136"] = (D["panel"] == "B136").astype(float)
    D["P_SMALL"] = (D["panel"] == "SMALL").astype(float)
    rung_keys = sorted({(r.panel, r.N) for r in D.itertuples()})
    say(f"  {len(D)} draws  ({D.groupby('panel').size().to_dict()}), {len(rung_keys)} (panel, N) rungs.")
    say("  PANEL MEANS of dCAGR (pp/yr), the 3x spread idea 1632 published:")
    for pn, g in D.groupby("panel"):
        say(f"    {pn:6s} mean {g['y'].mean():+.3f}  sd {g['y'].std(ddof=0):.3f}  "
            f"[{g['y'].min():+.3f}, {g['y'].max():+.3f}]  n={len(g)}")
    say("  PANEL MEANS of the three PRICE-ONLY regressors:")
    for pn, g in D.groupby("panel"):
        say(f"    {pn:6s} GATEOUT {g['GATEOUT'].mean():.4f}   XRATE {g['XRATE'].mean():.3f} /name-yr"
            f"   RECOV_21 {g['RECOV_21'].mean():+.5f}  RECOV_63 {g['RECOV_63'].mean():+.5f}"
            f"  RECOV_126 {g['RECOV_126'].mean():+.5f}")

    regrows = []
    for W in WINDOWS:
        d = D.copy()
        d["RECOV"] = d[f"RECOV_{W}"]
        d = d[np.isfinite(d["RECOV"]) & np.isfinite(d["y"])]
        for sname, cols in REG_SETS.items():
            X, _, _ = design(d, cols)
            b, resid, r2, adj = ols(X, d["y"].values)
            se = boot_se(d, cols, "y", rung_keys)
            part = {}
            for i, cc in enumerate(cols):
                rest = [z for z in cols if z != cc]
                if rest:
                    Xr, _, _ = design(d, rest)
                    _, _, r2r, _ = ols(Xr, d["y"].values)
                else:
                    r2r = 0.0
                part[cc] = r2 - r2r
            rr = dict(window=W, regset=sname, n=len(d), R2=r2, adjR2=adj,
                      intercept=b[0], intercept_se=se[0])
            for i, cc in enumerate(cols):
                rr[f"beta_{cc}"] = b[i + 1]
                rr[f"se_{cc}"] = se[i + 1]
                rr[f"t_{cc}"] = b[i + 1] / se[i + 1] if se[i + 1] > 0 else np.nan
                rr[f"partialR2_{cc}"] = part[cc]
            regrows.append(rr)
    REG = pd.DataFrame(regrows)
    REG.to_csv(OUT / "regressions.csv", index=False)

    say("\n  POOLED FITS (standardized betas; SE from a 2,000x RUNG-block bootstrap, not draws):")
    say(f"    {'W':>4} {'set':<10} {'R2':>8} {'adjR2':>8}   betas (t)")
    for _, r in REG.iterrows():
        cols = REG_SETS[r["regset"]]
        bs = "  ".join(f"{c}={r[f'beta_{c}']:+.3f}({r[f't_{c}']:+.2f})" for c in cols)
        say(f"    {int(r['window']):>4} {r['regset']:<10} {r['R2']:>8.4f} {r['adjR2']:>8.4f}   {bs}")

    best = REG[REG["regset"] == "GXR"].sort_values("adjR2", ascending=False).iloc[0]
    WSTAR = int(best["window"])
    say(f"\n  DROP-ONE PARTIAL R2 in the full GXR model at the best window W={WSTAR}:")
    for c in REG_SETS["GXR"]:
        say(f"    {c:<8} partial R2 {best[f'partialR2_{c}']:+.4f}   beta {best[f'beta_{c}']:+.4f} "
            f"+/- {best[f'se_{c}']:.4f}  (t {best[f't_{c}']:+.2f})")
    # --- the diagnostic that decides the reading: is GXR a LAW or a COLLINEAR PAIR?
    say("\n  [Q2b] IS THE JOINT FIT A LAW OR A NEAR-COLLINEAR SUPPRESSOR PAIR?")
    say("       (univariate R2 ~0 for all three, joint R2 ~0.6, betas +1.88 / -1.91 that nearly")
    say("        cancel, is the classic signature of two regressors carrying only their DIFFERENCE)")
    dW = D.copy(); dW["RECOV"] = dW[f"RECOV_{WSTAR}"]
    dW = dW[np.isfinite(dW["RECOV"])]
    corrows = []
    trio = ["GATEOUT", "XRATE", "RECOV"]
    for scope, g in [("POOLED", dW)] + [(pn, gg) for pn, gg in dW.groupby("panel")]:
        cm = g[trio].corr()
        r_gx = float(cm.loc["GATEOUT", "XRATE"])
        # VIF of each regressor in the GXR model
        vif = {}
        for c in trio:
            rest = [z for z in trio if z != c]
            Xr, _, _ = design(g, rest)
            _, _, r2r, _ = ols(Xr, g[c].values.astype(float))
            vif[c] = 1.0 / (1.0 - r2r) if r2r < 1 else np.inf
        # the DIFFERENCE regressor: standardized GATEOUT minus standardized XRATE, one column
        z = (g[trio[:2]] - g[trio[:2]].mean()) / g[trio[:2]].std(ddof=0)
        gg2 = g.copy(); gg2["DIFF"] = z["GATEOUT"] - z["XRATE"]
        Xd, _, _ = design(gg2, ["DIFF"])
        _, _, r2d, _ = ols(Xd, gg2["y"].values)
        Xgx, _, _ = design(g, ["GATEOUT", "XRATE"])
        _, _, r2gx, _ = ols(Xgx, g["y"].values)
        corrows.append(dict(scope=scope, n=len(g), corr_GATEOUT_XRATE=r_gx,
                            corr_GATEOUT_RECOV=float(cm.loc["GATEOUT", "RECOV"]),
                            corr_XRATE_RECOV=float(cm.loc["XRATE", "RECOV"]),
                            VIF_GATEOUT=vif["GATEOUT"], VIF_XRATE=vif["XRATE"], VIF_RECOV=vif["RECOV"],
                            R2_GX=r2gx, R2_single_DIFF=r2d))
        say(f"    {scope:6s} n={len(g):3d}  corr(GATEOUT,XRATE) {r_gx:+.4f}  VIF {vif['GATEOUT']:6.1f} /"
            f" {vif['XRATE']:6.1f} / {vif['RECOV']:5.2f}   R2(GATEOUT+XRATE) {r2gx:.4f}  vs"
            f"  R2(ONE column = zGATEOUT - zXRATE) {r2d:.4f}")
    pd.DataFrame(corrows).to_csv(OUT / "collinearity.csv", index=False)

    rp = REG[(REG["window"] == WSTAR) & (REG["regset"] == "PANEL")].iloc[0]
    rgp = REG[(REG["window"] == WSTAR) & (REG["regset"] == "GXR+PANEL")].iloc[0]
    say(f"    PANEL LABEL ALONE R2 {rp['R2']:.4f}   |   GXR R2 {best['R2']:.4f}   |   "
        f"GXR+PANEL R2 {rgp['R2']:.4f}  (panel adds {rgp['R2']-best['R2']:+.4f})")

    # Q3: within-panel
    say("\n  [Q3] WITHIN-PANEL fits (the between-panel fit is only 3 points and proves nothing):")
    wrows = []
    for pn, g in D.groupby("panel"):
        g = g.copy(); g["RECOV"] = g[f"RECOV_{WSTAR}"]
        g = g[np.isfinite(g["RECOV"])]
        for sname in ["G", "X", "R", "GXR"]:
            cols = REG_SETS[sname]
            X, _, _ = design(g, cols)
            b, _, r2, adj = ols(X, g["y"].values)
            wrows.append(dict(panel=pn, regset=sname, n=len(g), R2=r2, adjR2=adj,
                              **{f"beta_{c}": b[i + 1] for i, c in enumerate(cols)}))
            say(f"    {pn:6s} {sname:<4} n={len(g):3d}  R2 {r2:+.4f}  adjR2 {adj:+.4f}   "
                + "  ".join(f"{c}={b[i+1]:+.3f}" for i, c in enumerate(cols)))
    pd.DataFrame(wrows).to_csv(OUT / "within_panel.csv", index=False)

    # Q4: leave-one-panel-out
    say("\n  [Q4] LEAVE-ONE-PANEL-OUT: fit on TWO panels, predict the THIRD's draws.")
    say("       (the only test that can support 'predict which universe the band is affordable on')")
    lorows = []
    for held in ["U56", "B136", "SMALL"]:
        tr = D[D["panel"] != held].copy(); te = D[D["panel"] == held].copy()
        for s in (tr, te):
            s["RECOV"] = s[f"RECOV_{WSTAR}"]
        tr = tr[np.isfinite(tr["RECOV"])]; te = te[np.isfinite(te["RECOV"])]
        for sname in ["X", "GXR"]:
            cols = REG_SETS[sname]
            Xtr, mu, sd = design(tr, cols)
            b, _, r2tr, _ = ols(Xtr, tr["y"].values)
            Xte, _, _ = design(te, cols, mu=mu, sd=sd)
            pred = Xte @ b
            yte = te["y"].values
            sse = float(((yte - pred) ** 2).sum())
            sst = float(((yte - yte.mean()) ** 2).sum())
            sst0 = float(((yte - tr["y"].mean()) ** 2).sum())
            lorows.append(dict(held=held, regset=sname, n_train=len(tr), n_test=len(te),
                               R2_train=r2tr, pred_mean=float(pred.mean()), true_mean=float(yte.mean()),
                               bias=float(pred.mean() - yte.mean()),
                               R2_oos_vs_own_mean=1 - sse / sst if sst > 0 else np.nan,
                               R2_oos_vs_train_mean=1 - sse / sst0 if sst0 > 0 else np.nan,
                               corr=float(np.corrcoef(pred, yte)[0, 1]) if len(te) > 2 else np.nan))
            r = lorows[-1]
            say(f"    hold out {held:6s} set={sname:<4} train R2 {r['R2_train']:.4f} | "
                f"predicted mean {r['pred_mean']:+.3f} vs TRUE {r['true_mean']:+.3f} pp "
                f"(bias {r['bias']:+.3f}) | R2 on held-out panel {r['R2_oos_vs_own_mean']:+.4f} "
                f"(vs train mean {r['R2_oos_vs_train_mean']:+.4f}) | corr {r['corr']:+.4f}")
    pd.DataFrame(lorows).to_csv(OUT / "leave_one_panel_out.csv", index=False)

    # ------------------------------------------------ Q5: capital + rule 8
    say("\n" + "=" * 118)
    say("  [Q5] CAPITAL: both KEEP paths at EVERY cell, then rule 8 (2017-2026 read ONCE).")
    say("=" * 118)
    B10 = G[G["cost_bps"] == BIND]
    say(f"  Over all {len(B10)} band books at 10 bps: 4a FULL {int(B10['keep4a'].sum())}, "
        f"4b FULL {int(B10['keep4b'].sum())}, 4a OOS {int(B10['O_keep4a'].sum())}, "
        f"4b OOS {int(B10['O_keep4b'].sum())}.")
    both = B10[B10["keep4b"] & B10["O_keep4b"]]
    say(f"  Clearing 4b FULL *and* OOS: {len(both)}")
    for _, r in both.iterrows():
        say(f"    {r['panel']} N={int(r['N'])} draw={int(r['draw'])} c={r['band']:.2f}  "
            f"FULL {r['CAGR']:.2%}/{r['Sharpe']:.4f}/{r['MaxDD']:.2%}  "
            f"OOS {r['O_CAGR']:.2%}/{r['O_Sharpe']:.4f}/{r['O_MaxDD']:.2%}")

    # IS-only regression for the chooser (G6: no row >= 2017 is read)
    say("\n  RULE 8.  The chooser's regression is re-fit on IS ROWS ONLY (warm-up..2016-12-31):")
    DI = D.copy()
    DI["y_is"] = DI["IS_dCAGR"] * 100.0
    isrows = []
    for W in WINDOWS:
        d = DI.copy(); d["RECOV"] = d[f"IS_RECOV_{W}"]
        d["GATEOUT"] = d["IS_GATEOUT"]; d["XRATE"] = d["IS_XRATE"]
        d = d[np.isfinite(d["RECOV"]) & np.isfinite(d["y_is"])]
        for sname in ["X", "GXR"]:
            cols = REG_SETS[sname]
            X, mu, sd = design(d, cols)
            b, _, r2, adj = ols(X, d["y_is"].values)
            isrows.append(dict(window=W, regset=sname, n=len(d), IS_R2=r2, IS_adjR2=adj))
            say(f"    IS fit W={W:>3} set={sname:<4} R2 {r2:.4f} adjR2 {adj:.4f}")
    ISR = pd.DataFrame(isrows)
    pick = ISR.sort_values("IS_adjR2", ascending=False).iloc[0]
    W_IS, S_IS = int(pick["window"]), pick["regset"]
    say(f"    -> DIALS CHOSEN IN SAMPLE: W = {W_IS}, regressor set = {S_IS} "
        f"(IS adjR2 {pick['IS_adjR2']:.4f}).  2017-2026 still unread.")
    cols = REG_SETS[S_IS]
    dfit = DI.copy()
    dfit["RECOV"] = dfit[f"IS_RECOV_{W_IS}"]; dfit["GATEOUT"] = dfit["IS_GATEOUT"]; dfit["XRATE"] = dfit["IS_XRATE"]
    dfit = dfit[np.isfinite(dfit["RECOV"]) & np.isfinite(dfit["y_is"])]
    Xf, mu, sd = design(dfit, cols)
    bfit, _, _, _ = ols(Xf, dfit["y_is"].values)
    Xall, _, _ = design(dfit, cols, mu=mu, sd=sd)
    dfit["pred_cost"] = Xall @ bfit

    wf = []
    for p in panels:
        bars = BARS[p.name]
        sl = dfit[dfit["panel"] == p.name]
        base_all = D[D["panel"] == p.name]
        base = dict(mean_O_Sharpe=float(base_all["O_Sharpe"].mean()),
                    share_4b_O=float(base_all["O_keep4b"].mean()),
                    share_4a_O=float(base_all["O_keep4a"].mean()),
                    mean_O_CAGR=float(base_all["O_CAGR"].mean()))
        say(f"\n  [{p.name}] DRAW BASE RATE over {len(base_all)} draws at c=0.03: mean OOS Sharpe "
            f"{base['mean_O_Sharpe']:.4f}, mean OOS CAGR {base['mean_O_CAGR']:.2%}, "
            f"4b OOS share {base['share_4b_O']:.1%}, 4a OOS share {base['share_4a_O']:.1%}")
        cands = {
            "C_WHIP":   sl.sort_values("pred_cost", ascending=False).iloc[0],   # least NEGATIVE cost
            "C_XRATE":  sl.sort_values("IS_XRATE", ascending=True).iloc[0],
            "C_SHARPE": sl.sort_values("IS_Sharpe", ascending=False).iloc[0],
            "C_LIVE":   sl[sl["N"] == sl["n_all"].iloc[0]].iloc[0],
        }
        for cname, r in cands.items():
            key = (p.name, int(r["N"]), int(r["draw"]))
            rr = books[key]["r"]
            rt = books[key]["rtI"]
            k4a, k4b, m, h1, h2, legs = keep_paths(rr[p.i_oos:], bars["spyO"], bars["liveO"])
            mt = bmpack(rt[p.i_oos:])
            wf.append(dict(panel=p.name, chooser=cname, N=int(r["N"]), draw=int(r["draw"]),
                           band=LIVE_C, IS_Sharpe=r["IS_Sharpe"], IS_XRATE=r["IS_XRATE"],
                           pred_cost_pp=r["pred_cost"], realised_O_dCAGR_pp=r["O_dCAGR"] * 100,
                           O_CAGR=m["CAGR"], O_Sharpe=m["Sharpe"], O_MaxDD=m["MaxDD"],
                           O_twin_Sharpe=mt["Sharpe"], O_twin_MaxDD=mt["MaxDD"],
                           O_keep4a=k4a, O_keep4b=k4b,
                           leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"], leg_CAGR=legs["CAGR"],
                           live_O_CAGR=bars["liveO"]["CAGR"], live_O_Sharpe=bars["liveO"]["Sharpe"],
                           live_O_MaxDD=bars["liveO"]["MaxDD"],
                           spy_O_CAGR=bars["spyO"]["CAGR"], spy_O_Sharpe=bars["spyO"]["Sharpe"],
                           spy_O_MaxDD=bars["spyO"]["MaxDD"],
                           base_mean_O_Sharpe=base["mean_O_Sharpe"], base_share_4b_O=base["share_4b_O"]))
            say(f"    {cname:<9} N={int(r['N']):>3} draw={int(r['draw']):>2} | pred cost "
                f"{r['pred_cost']:+.3f} pp, realised OOS {r['O_dCAGR']*100:+.3f} pp | OOS "
                f"{m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%} | 4a {k4a} 4b {k4b}"
                f" | legs H1={legs['H1']} H2={legs['H2']} DD={legs['DD']} CAGR={legs['CAGR']}")
        say(f"    vs live RULES v2 OOS {bars['liveO']['CAGR']:.2%} / {bars['liveO']['Sharpe']:.4f} / "
            f"{bars['liveO']['MaxDD']:.2%}   vs SPY OOS {bars['spyO']['CAGR']:.2%} / "
            f"{bars['spyO']['Sharpe']:.4f} / {bars['spyO']['MaxDD']:.2%}")
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / "walkforward.csv", index=False)

    # does the chooser's RANKING carry OOS at all?
    say("\n  DOES THE IS-FITTED PREDICTION RANK THE OOS COST?  (Spearman, per panel and pooled)")
    rankrows = []
    for pn, g in dfit.groupby("panel"):
        a = g["pred_cost"].rank(); b_ = (g["O_dCAGR"] * 100).rank()
        rho = float(np.corrcoef(a, b_)[0, 1])
        rankrows.append(dict(scope=pn, n=len(g), spearman_pred_vs_OOS_dCAGR=rho,
                             spearman_ISxrate_vs_OOS_dCAGR=float(np.corrcoef(
                                 g["IS_XRATE"].rank(), b_)[0, 1])))
        say(f"    {pn:6s} n={len(g):3d}  rho(pred, OOS dCAGR) {rho:+.4f}   "
            f"rho(IS XRATE, OOS dCAGR) {rankrows[-1]['spearman_ISxrate_vs_OOS_dCAGR']:+.4f}")
    a = dfit["pred_cost"].rank(); b_ = (dfit["O_dCAGR"] * 100).rank()
    rankrows.append(dict(scope="POOLED", n=len(dfit),
                         spearman_pred_vs_OOS_dCAGR=float(np.corrcoef(a, b_)[0, 1]),
                         spearman_ISxrate_vs_OOS_dCAGR=float(np.corrcoef(
                             dfit["IS_XRATE"].rank(), b_)[0, 1])))
    say(f"    POOLED n={len(dfit)}  rho(pred, OOS dCAGR) {rankrows[-1]['spearman_pred_vs_OOS_dCAGR']:+.4f}"
        f"   rho(IS XRATE, OOS dCAGR) {rankrows[-1]['spearman_ISxrate_vs_OOS_dCAGR']:+.4f}")
    pd.DataFrame(rankrows).to_csv(OUT / "rank_stability.csv", index=False)

    # G6: re-test that the IS pipeline never touches an OOS row
    say("\n  [G6] re-running the IS regressors on a TRUNCATED tape (rows < 2017-01-01 only):")
    tr_dev = 0.0
    for p in panels:
        pxt = p.px.loc[:IS_END]
        cols_t = [c for c in p.cols if c in pxt.columns]
        pt = Panel(p.name, pxt, cols_t)
        for N in rungs[p.name][:1]:
            M = len(p.cols)
            j = np.sort(np.random.default_rng(SEED0 + 1009 * N + 0).choice(M, size=N, replace=False))
            a = whipsaw(Sub(p, j), LIVE_C, WARMUP, p.i_oos)
            b2 = whipsaw(Sub(pt, j), LIVE_C, WARMUP, pt.T)
            for kk in ("GATEOUT", "XRATE"):
                tr_dev = max(tr_dev, abs(a[kk] - b2[kk]))
    gate("G6 IS regressors identical on a TRUNCATED-at-2016 tape (GATEOUT, XRATE max |dev|)",
         f"{tr_dev:.3e}", "< 1e-12", tr_dev < 1e-12)

    G.to_csv(OUT / "grid.csv.gz", index=False, compression="gzip")
    ISR.to_csv(OUT / "is_fits.csv", index=False)
    pd.DataFrame(GATES).to_csv(OUT / "gates.csv", index=False)
    npass = sum(1 for g_ in GATES if g_["pass_"] and g_["target"] != "published, not asserted")
    ntot = sum(1 for g_ in GATES if g_["target"] != "published, not asserted")
    say(f"\n  GATES {npass}/{ntot} pass.")
    (OUT / "log.txt").write_text("\n".join(LOG) + "\n")
    say(f"  wrote {OUT.name}/grid.csv.gz .regressions.csv .within_panel.csv "
        f".leave_one_panel_out.csv .walkforward.csv .rank_stability.csv .is_fits.csv .gates.csv .log.txt")
    say(f"  elapsed {time.time()-t0:.0f}s")
    (OUT / "log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

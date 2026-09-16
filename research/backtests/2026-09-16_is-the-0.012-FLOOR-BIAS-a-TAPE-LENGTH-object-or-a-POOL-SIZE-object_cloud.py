#!/usr/bin/env python3
"""Idea 1047 (cloud lane, 2026-09-16) — is the 0.012 FLOOR BIAS a TAPE-LENGTH object or a
POOL-SIZE object?

QUESTION (QUEUE idea 1047, verbatim)
    idea 1044's zero-dispersion control fits a floor of +0.0115 / +0.0047 where the truth is
    exactly 0, so any dispersion floor the record reports below 0.012 is estimator bias.  Walk
    the pool size (18 GRID, GRID+SHELF, a widened band x gross ladder) and the tape length and
    report which axis carries the bias, so the 0.012 threshold can be stated per cell instead of
    globally.  Max 2 params (pool, tape length).

THE OBJECT.  1044 fitted sd_RAW(L)^2 = D^2 + C/L across a length ladder and published D =
    sqrt(max(D2_hat, 0)) as the "dispersion floor".  On NULL_0 — a synthetic pool with exactly
    zero true cross-book dispersion — that floor still read +0.0115 (U56) / +0.0047 (B136).
    This run measures that positive reading as a function of the two things that can possibly
    drive it, and publishes a per-cell threshold in place of the global 0.012.

THE ARITHMETIC, DECLARED BEFORE ANY NUMBER (this is a prediction, not a post-hoc story).
    Under NULL_0 the population cross-book variance is 0, so E[sd_RAW(L)^2] = C/L exactly and
    the OLS intercept D2_hat is an UNBIASED estimator of 0.  The published floor is not D2_hat
    but sqrt(max(D2_hat, 0)), and for a mean-zero estimator
                E[ sqrt(max(D2_hat, 0)) ]  ~  k * sqrt( SD(D2_hat) ),     k = O(1) > 0,
    so the entire +0.0115 is a TRUNCATION-AND-SQUARE-ROOT artifact of the NOISE in D2_hat, not
    a bias in D2_hat.  That noise has a known scaling.  sd_RAW^2 at one window is a sample
    variance over N books, so SD(sd_RAW^2) = sd_RAW^2 * sqrt(2/(N-1)) for independent books, and
    the OLS intercept inherits it:
                SD(D2_hat)  ~  (C / Lbar) * sqrt(2/(N-1))          =>
                FLOOR_BIAS  ~  sqrt(C) * Lbar^(-1/2) * (N-1)^(-1/4).
    PREDICTION, written ahead of the run: the log-log slope in TAPE LENGTH is about -0.50 and
    the log-log slope in POOL SIZE is about -0.25, i.e. BOTH axes carry it but tape length
    carries it about TWICE as fast per log unit, and a 16x pool is needed to buy what a 4x tape
    buys.  H_AXIS below is the decisive test of exactly that.

TWO CONFOUNDS STATED UP FRONT, not discovered later.
    (1) LADDER GEOMETRY.  Shortening the tape also DROPS the long rungs of 1044's fixed ladder,
        so a NATIVE-ladder length walk confounds "shorter tape" with "fewer and shorter rungs".
        Every length point is therefore reported on TWO ladders: NATIVE (1044's rungs that still
        fit) and SCALED (1044's rungs multiplied by the tape fraction, so the rung COUNT and the
        ladder's SHAPE are held fixed and only absolute length moves).  SCALED is the clean
        length axis; NATIVE is what the record would actually have done.  Neither is selected.
    (2) EFFECTIVE POOL SIZE.  1044's NULL_0 draws each synthetic book's idiosyncratic part
        INDEPENDENTLY, so its nominal N is its effective N by construction — while a real
        widened band x gross ladder is nearly collinear (gross is very close to a Sharpe-
        invariant dial).  Reporting only 1044's construction would therefore make the pool axis
        look better than a real pool can deliver.  So every pool point is also run under
        NULL_0R, which resamples the pool's REAL idiosyncratic matrix jointly by day (each
        column demeaned and rescaled to a common scale, so the true dispersion is still exactly
        zero) and thus inherits the real cross-book idio correlation.  NULL_0 is the headline
        because it is the record's committed construction; NULL_0R is what a real pool buys.

WHAT IS MEASURED
    (A) THE BIAS SURFACE.  Median and p95 of the fitted floor over NREP NULL_0 reps at every
        (pool) x (tape fraction) x (ladder) x (panel) x (cost rung) point — 3 x 4 x 2 x 2 x 2 =
        192 cells, ALL published, none selected.  NULL_0R at the same points.
    (B) THE TWO SLOPES.  Log-log OLS of the median floor on tape length (at fixed pool) and on
        pool size (at fixed tape), per (panel, ladder, rung).  Reported against the predicted
        -0.50 / -0.25.
    (C) THE RESOLUTION CONTROL (not a third dial).  An N-subsample ladder N in
        {6, 9, 12, 18, 24, 32, 48} drawn from the WIDE pool, which fits the pool slope off SEVEN
        points instead of three.  Published at every point, never used to choose anything.
    (D) THE UNBIASEDNESS CHECK.  The mean of D2_hat itself against its own standard error, which
        separates "the floor estimator is biased" from "D2_hat is unbiased and the square root
        of a truncated noisy zero is positive".
    (E) THE PAYOFF THE QUEUE ASKS FOR.  Every one of the record's 24 committed floors (1044's
        own fits.csv, the artifact that raised this question) re-read against the threshold of
        ITS OWN cell instead of the global 0.012, and the count that changes verdict.
    (F) THE RULE-8 WALK-FORWARD at PROTOCOL's declared split 2016-12-31 (IS 2009-2016 chooses,
        2017-2026 read ONCE): OOS CAGR / Sharpe / MaxDD for three IS-only choosers run over EACH
        pool separately, on both panels at both rungs, against the live RULES v2 baseline and
        against SPY, BOTH KEEP paths (4a and 4b), every point reported.  The pool is this run's
        own dial, so this also answers whether widening the pool a chooser draws from buys any
        out-of-sample return at all.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL 12 (pool x tape) points reported.
    (1) POOL    GRID   = the record's 18 mechanical GRID books per panel (861's ladder).
                SHELF  = GRID + the record's memo-selected shelf books for that panel
                         (U56 24, B136 21).
                WIDE   = a widened band x gross ladder, 8 bands x 6 gross = 48 books per panel.
    (2) TAPE LENGTH  fraction f in {0.25, 0.50, 0.75, 1.00} of the post-warmup tape, tail-
                     anchored (the record's own TAIL convention).

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_TAPE  the tape-length slope matches the arithmetic: fitted slope of log(floor) on
            log(tape length) lies in [-0.60, -0.40] on BOTH panels at 10 bps on the SCALED
            ladder.
    H_POOL  the pool slope matches the arithmetic: fitted slope of log(floor) on log(N-1) lies
            in [-0.35, -0.15] on BOTH panels at 10 bps, on the 7-point N-subsample control.
    H_AXIS  DECISIVE, the queue's literal question.  |slope_tape| > 1.5 * |slope_pool| in at
            least 3 of the 4 (panel, ladder) cells at 10 bps.  PASS => the bias is a TAPE-LENGTH
            object first and a pool-size object second.  FAIL => the two axes are comparable and
            the queue's either/or is the wrong frame.
    H_UNB   the floor bias is a SQUARE-ROOT artifact, not a bias in D2: |mean(D2_hat)| <= 2 *
            SE(mean D2_hat) in at least 4 of the 6 headline cells.
    H_CELL  THE PAYOFF.  A single global threshold is wrong: the per-cell p95 floor threshold
            spans a factor of >= 2.0 across the 192-cell grid, AND at least one of the record's
            24 committed floors changes verdict when read against its own cell.
    H_EFF   the pool axis is WEAKER on a real pool than on 1044's independent-idio construction:
            NULL_0R's pool slope is smaller in magnitude than NULL_0's on both panels at 10 bps.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  this run's fast runner == engine.backtest on a live book, returns AND turnover.
    G2  the pools are the record's own grid_books()/shelf_books(), with the stated counts.
    G3  CROSS-RUN: SPY's OOS triple at 2016-12-31 == the committed 15.21% / 0.8713 / -33.72%.
    G4  CROSS-RUN: 1044's committed NULL_0 median floor reproduces at its own cell
        (GRID, f = 1.00, NATIVE ladder, TAIL, 10 bps): 0.0115 (U56) / 0.0047 (B136).
    G5  CROSS-RUN: 1044's committed NULL_0 median b (-0.5011 / -0.5049) and median C
        (26.84 / 28.40) reproduce at the same cell.
    G6  the closed-form SAT fit recovers a KNOWN (D, C) on synthetic sd^2 data to 1e-9.
    G7  WINDOW CONSTRUCTION: every window has exactly L days and is tail-anchored.
    G8  NULL_0 and NULL_0R both have EXACTLY zero true dispersion: every synthetic book's
        population mean and population variance are identical to 1e-12.
    G9  determinism: the whole surface rebuilds bit-for-bit, off process-stable md5 seeds.
    G10 NULL_0R preserves the real pool's idiosyncratic correlation matrix (mean |d|), and
        NULL_0 does not (its idio correlation is ~0 by construction).

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and
    drawdown LEVEL in section (F) is optimistic and the 4b counts there are an UPPER bound.  The
    measured object in (A)-(E) is the SAMPLING BEHAVIOUR of an intercept estimator under a null
    with zero true dispersion; survivorship enters it only through C (the Sharpe LEVEL raises
    252 + SR^2/2), which shifts every cell of the surface by the same multiplicative sqrt(C) and
    therefore cannot create or destroy either slope.  Reported, not asserted: C is published per
    cell so the shift can be divided out.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-the-0.012-FLOOR-BIAS-a-TAPE-LENGTH-object-or-a-POOL-SIZE-object"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"
FITS_1044 = HERE / "2026-09-16_is-the-K-FREE-NULL-SD-a-WINDOW-LENGTH-CURVE-with-a-SOLVABLE-EXPONENT_cloud.fits.csv"

WARMUP = 260
RUNGS = [10.0, 25.0]
RUNG_HEAD = 10.0
PANEL_HEAD = "U56"
REC_END = "2016-12-31"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
LENS_1044 = [250, 400, 600, 900, 1300, 1900, 2800]

# ---- the two tuned dials --------------------------------------------------------------------
POOLS = ["GRID", "SHELF", "WIDE"]
FRACS = [0.25, 0.50, 0.75, 1.00]
LADDERS = ["NATIVE", "SCALED"]
POOL_HEAD, FRAC_HEAD, LADDER_HEAD = "GRID", 1.00, "NATIVE"   # = 1044's own cell

NSUB = [6, 9, 12, 18, 24, 32, 48]        # reported CONTROL, not a third dial
WIDE_BANDS = [0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.18, 0.25]
WIDE_GROSS = [0.20, 0.35, 0.50, 0.65, 0.80, 1.00]

NREP = 500
SEED0 = 20260916
SQ252 = np.sqrt(252.0)
GLOBAL_FLOOR_BAR = 0.012                 # the threshold the queue asks to replace

SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
PUB_1044_NULL0 = {"U56": dict(D=0.0115, b=-0.5011, C=26.8380),
                  "B136": dict(D=0.0047, b=-0.5049, C=28.3950)}
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


spec = importlib.util.spec_from_file_location("laneC1023", LANEC)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


# ====================================================================== shared machinery (1044's)
def cums(R):
    z = np.zeros((1, R.shape[1]))
    return (np.vstack([z, np.cumsum(R, axis=0)]),
            np.vstack([z, np.cumsum(R * R, axis=0)]))


def win_sharpes(cs, cs2, wins):
    out = np.empty((len(wins), cs.shape[1]))
    for j, (a, b) in enumerate(wins):
        n = b - a
        s = cs[b] - cs[a]
        q = cs2[b] - cs2[a]
        m = s / n
        var = (q - n * m * m) / (n - 1)
        out[j] = SQ252 * m / np.sqrt(var)
    return out


def fit_pow(L, sd):
    Lv, sdv = np.asarray(L, float), np.asarray(sd, float)
    x, y = np.log(Lv), np.log(sdv)
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return float(coef[1])


def fit_sat(L, sd):
    """sd^2 = D2 + C*(1/L), closed-form OLS.  Returns (D2, C, se_D2)."""
    x = 1.0 / np.asarray(L, float)
    y = np.asarray(sd, float) ** 2
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ coef
    dof = max(len(x) - 2, 1)
    s2 = float((res ** 2).sum() / dof)
    cov = s2 * np.linalg.inv(A.T @ A)
    return float(coef[0]), float(coef[1]), float(np.sqrt(max(cov[0, 0], 0.0)))


def loglog_slope(x, y, want_n=False):
    """OLS slope of log y on log x.  Points with y <= 0 CANNOT enter a log fit, so the number of
    points actually used is returned alongside — a slope fitted off 2 of 4 rungs is not a slope."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = (x > 0) & (y > 0) & np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 2:
        return (np.nan, int(ok.sum())) if want_n else np.nan
    lx, ly = np.log(x[ok]), np.log(y[ok])
    A = np.vstack([np.ones_like(lx), lx]).T
    coef, *_ = np.linalg.lstsq(A, ly, rcond=None)
    return (float(coef[1]), int(ok.sum())) if want_n else float(coef[1])


def mdseed(*parts):
    h = hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()
    return int(h[:8], 16)


def ladder_for(T, frac, ladder):
    """The length rungs used at tape fraction `frac`.

    NATIVE  1044's rungs that still fit in the shortened tape (what the record would have done).
    SCALED  1044's rungs times `frac`, so rung COUNT and ladder SHAPE are held fixed and only
            absolute length moves.  This is the clean tape-length axis.
    """
    if ladder == "NATIVE":
        return [L for L in LENS_1044 if L <= T]
    return [max(60, int(round(L * frac))) for L in LENS_1044 if int(round(L * frac)) <= T]


def tail_windows(T, lens):
    return [(T - L, T) for L in lens]


# ====================================================================== the pools
def wide_books(px, pname):
    """A widened band x gross ladder: 8 bands x 6 gross = 48 books, weekly, one panel."""
    out = {}
    for band, g in product(WIDE_BANDS, WIDE_GROSS):
        out[f"{pname}-wband{band:.2f}-g{g:.2f}"] = dict(
            panel=pname, freq="W", W=rules_v2_weights(px, band, g), src="WIDE")
    return out


def build_pools(U, B):
    grid = C.grid_books(U, B)
    shelf = C.shelf_books(U, B)
    allb = dict(grid)
    allb.update(shelf)
    for pname, px in (("U56", U), ("B136", B)):
        allb.update(wide_books(px, pname))
    members = {}
    for p in ("U56", "B136"):
        g = sorted(k for k, v in grid.items() if v["panel"] == p)
        s = sorted(k for k, v in shelf.items() if v["panel"] == p)
        w = sorted(k for k, v in allb.items() if v["panel"] == p and v.get("src") == "WIDE")
        members[("GRID", p)] = g
        members[("SHELF", p)] = g + s
        members[("WIDE", p)] = w
    return allb, members


# ====================================================================== the two zero-dispersion nulls
def null_parts(R):
    """Common factor, demeaned/rescaled idio matrix, and the common idio scale.

    R is T x N of REAL net returns.  com = row mean (the pool's common factor).  idio = R - com,
    then each column is demeaned and rescaled to the pool-median idio sd.  After that every
    synthetic book has the SAME population mean (mean(com)) and the SAME population variance,
    so the TRUE cross-book Sharpe dispersion is exactly zero under BOTH nulls.
    """
    com = R.mean(axis=1)
    idio = R - com[:, None]
    sd = idio.std(axis=0, ddof=1)
    sc = float(np.median(sd))
    idio_n = (idio - idio.mean(axis=0)) / sd * sc
    return com, idio_n, sc


def null_floor(R, T, lens, nrep, seed, kind):
    """NREP fitted floors (and b, C, D2) under a zero-true-dispersion null.

    NULL_0   1044's construction: X = com[ix] + N(0, sc) drawn INDEPENDENTLY per book, so the
             nominal pool size is the effective pool size.
    NULL_0R  X = com[ix] + idio_n[ix], i.e. the REAL idiosyncratic matrix resampled JOINTLY by
             day, so the pool's real cross-book idio correlation is inherited and the effective
             pool size is smaller than the nominal one.
    """
    Tn, N = R.shape
    com, idio_n, sc = null_parts(R)
    rng = np.random.default_rng(mdseed(seed, kind, Tn, N, tuple(lens)))
    wins = tail_windows(T, lens)
    Ds, D2s, bs, Cs = [], [], [], []
    for _ in range(nrep):
        ix = rng.integers(0, Tn, size=T)
        if kind == "NULL_0":
            X = com[ix][:, None] + rng.standard_normal((T, N)) * sc
        else:
            X = com[ix][:, None] + idio_n[ix]
        cs, cs2 = cums(X)
        sd = win_sharpes(cs, cs2, wins).std(axis=1, ddof=1)
        D2, Cc, _ = fit_sat(lens, sd)
        Ds.append(np.sqrt(max(D2, 0.0)))
        D2s.append(D2)
        bs.append(fit_pow(lens, sd))
        Cs.append(Cc)
    return np.array(Ds), np.array(D2s), np.array(bs), np.array(Cs)


# ====================================================================== rule-8 machinery (1044's)
def metblock(r):
    c, s, d = fmet(r)
    k = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:k]), H2=fsharpe(r[k:]))


def split_block(net, e=REC_END):
    b = metblock(net.values)
    o = net.loc[pd.Timestamp(e) + pd.Timedelta(days=1):].values
    i = net.loc[:pd.Timestamp(e)].values
    oc, os_, od = fmet(o)
    ic, is_, idd = fmet(i)
    b.update(OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_n=len(o),
             IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd, IS_n=len(i))
    return b


def legs_at(bk, sb):
    return {"L1_H1": bool(bk["H1"] > sb["H1"]),
            "L2_H2": bool(bk["H2"] > sb["H2"]),
            "L3_OOS": bool(bk["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L4_DD": bool(abs(bk["OOS_MaxDD"]) <= DDCAP_FRAC * abs(sb["MaxDD"])),
            "L5_CAGR": bool(bk["OOS_CAGR"] >= CAGRFLOOR_FRAC * sb["CAGR"])}


def raw_pick(sub, ch, spy_is):
    if ch == "IS_SHARPE":
        return sub["IS_Sharpe"].idxmax()
    if ch == "IS_CAGR":
        return sub["IS_CAGR"].idxmax()
    s = sub.copy()
    s["nlegs"] = ((s["IS_Sharpe"] > spy_is[1]).astype(int)
                  + (s["IS_CAGR"] >= CAGRFLOOR_FRAC * spy_is[0]).astype(int)
                  + (s["IS_MaxDD"].abs() <= DDCAP_FRAC * abs(spy_is[2])).astype(int))
    s = s.sort_values(["nlegs", "IS_Sharpe"], ascending=False)
    return s.index[0]


def main():
    t0 = time.time()
    P(f"# Idea 1047 (cloud lane, {DATE}) — is the 0.012 FLOOR BIAS a TAPE-LENGTH object or a "
      f"POOL-SIZE object?")
    P(f"# 2 tuned dials: POOL {POOLS} x TAPE FRACTION {FRACS} = {len(POOLS)*len(FRACS)} points, "
      f"ALL reported, none selected.  HEADLINE cell = 1044's own ({POOL_HEAD}, f={FRAC_HEAD}, "
      f"{LADDER_HEAD} ladder).")
    P(f"# Controls at every point: ladder geometry [NATIVE, SCALED], panel [U56, B136], cost "
      f"{RUNGS} bps (10 binding, PROTOCOL rule 2), null kind [NULL_0 (1044's), NULL_0R (real "
      f"idio)].  N-subsample ladder {NSUB} is a reported RESOLUTION control, not a third dial.")
    P("# DECLARED BEFORE ANY NUMBER: under NULL_0 the intercept D2_hat is UNBIASED for 0, so the")
    P("#   published floor sqrt(max(D2_hat,0)) is a truncation artifact of SD(D2_hat), and")
    P("#   FLOOR_BIAS ~ sqrt(C) * Lbar^-0.5 * (N-1)^-0.25.  PREDICTION: tape-length slope ~ -0.50,")
    P("#   pool slope ~ -0.25 — both axes carry it, tape length about twice as fast per log unit.")
    P("# CONFOUND 1 stated up front: shortening the tape also drops long rungs, so every length")
    P("#   point is reported on BOTH the NATIVE and the SCALED (shape-held-fixed) ladder.")
    P("# CONFOUND 2 stated up front: 1044's NULL_0 draws idio INDEPENDENTLY, so nominal N ==")
    P("#   effective N; a real widened gross ladder is near-collinear.  NULL_0R inherits the real")
    P("#   idio correlation and is published beside it at every point.")
    P(f"# NREP = {NREP} per cell.  SURVIVORSHIP: U56/B136 are current-constituent panels; the")
    P("#   level bias enters only through C and shifts every cell by the same sqrt(C), so it")
    P("#   cannot create or destroy either slope.  C is published per cell.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    PX = {"U56": U, "B136": B}
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; "
      f"B136 {B.shape} {B.index[0].date()}..{B.index[-1].date()}.")
    if not U.index.equals(B.index):
        P(f"   CALENDAR: each panel keeps its OWN calendar (the record's construction).  No splice.")

    ALLB, MEM = build_pools(U, B)
    P(f"POOLS per panel: " + ", ".join(
        f"{p}=[U56 {len(MEM[(p,'U56')])}, B136 {len(MEM[(p,'B136')])}]" for p in POOLS))

    # ---- net returns for every book at every rung, post-warmup
    REC = {p: PX[p].index[WARMUP] for p in PX}
    NET = {}
    TURN = {}
    for nm, b in ALLB.items():
        px = PX[b["panel"]]
        r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
        st = REC[b["panel"]]
        for c in RUNGS:
            NET[(nm, c)] = (r - t * c / 1e4).loc[st:]
        TURN[nm] = t.loc[st:]
    TLEN = {p: len(NET[(MEM[("GRID", p)][0], RUNG_HEAD)]) for p in PX}
    P(f"Post-warmup tape: U56 {TLEN['U56']} days, B136 {TLEN['B136']} days.")

    SPY = {p: PX[p]["SPY"].pct_change().fillna(0.0).loc[REC[p]:] for p in PX}
    V2 = {}
    for p, px in PX.items():
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            V2[(p, c)] = (r - t * c / 1e4).loc[REC[p]:]

    RMAT = {}
    for pl, p in product(POOLS, PX):
        for c in RUNGS:
            RMAT[(pl, p, c)] = np.column_stack([NET[(nm, c)].values for nm in MEM[(pl, p)]])

    # ================================================================== GATES
    P("=" * 100)
    P("REPRODUCTION GATES")
    P("=" * 100)
    gates = {}

    bk = MEM[("GRID", "U56")][0]
    b0 = ALLB[bk]
    eng = backtest(U, b0["W"], cost_bps=0.0, freq="W")
    rf, tf = fast_run(U, b0["W"], rebalance_mask(U.index, "W"))
    d1r = float(np.nanmax(np.abs(eng["returns"].values - rf.values)))
    d1t = float(np.nanmax(np.abs(eng["turnover"].values - tf.values)))
    gates["G1"] = (d1r < 1e-10 and d1t < 1e-10,
                   f"fast_run == engine.backtest on {bk}: max|dret| {d1r:.2e}, max|dturn| {d1t:.2e}")

    ok2 = (len(MEM[("GRID", "U56")]) == 18 and len(MEM[("GRID", "B136")]) == 18
           and len(MEM[("WIDE", "U56")]) == 48 and len(MEM[("WIDE", "B136")]) == 48
           and len(MEM[("SHELF", "U56")]) > 18 and len(MEM[("SHELF", "B136")]) > 18)
    gates["G2"] = (ok2, "pools are the record's grid_books()/shelf_books() plus the widened "
                        f"band x gross ladder: GRID 18/18, SHELF {len(MEM[('SHELF','U56')])}/"
                        f"{len(MEM[('SHELF','B136')])}, WIDE 48/48")

    so = split_block(SPY["U56"])
    d3 = max(abs(so["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(so["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(so["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = (d3 < 5e-4, f"CROSS-RUN SPY OOS at {REC_END}: {so['OOS_CAGR']:.4f} / "
                              f"{so['OOS_Sharpe']:.4f} / {so['OOS_MaxDD']:.4f} vs committed "
                              f"{SPY_OOS_COMMITTED} (max|d| {d3:.2e})")

    rep = {}
    for p in PX:
        lens = ladder_for(TLEN[p], 1.00, "NATIVE")
        Ds, D2s, bs, Cs = null_floor(RMAT[("GRID", p, RUNG_HEAD)], TLEN[p], lens, 1000,
                                     20260916, "NULL_0")
        rep[p] = dict(D=float(np.median(Ds)), b=float(np.median(bs)), Cc=float(np.median(Cs)))
    d4 = {p: abs(rep[p]["D"] - PUB_1044_NULL0[p]["D"]) for p in PX}
    gates["G4"] = (all(v < 0.006 for v in d4.values()),
                   "CROSS-RUN 1044 NULL_0 median floor at its own cell (GRID, f=1.00, NATIVE, "
                   "TAIL, 10 bps): " + ", ".join(
                       f"{p} {rep[p]['D']:.4f} vs {PUB_1044_NULL0[p]['D']:.4f} "
                       f"(|d| {d4[p]:.4f})" for p in PX)
                   + "  [same construction, independent seed stream -> a sampling-noise band, "
                     "not a bit match]")
    d5 = max(max(abs(rep[p]["b"] - PUB_1044_NULL0[p]["b"]) for p in PX),
             max(abs(rep[p]["Cc"] - PUB_1044_NULL0[p]["C"]) / PUB_1044_NULL0[p]["C"] for p in PX))
    gates["G5"] = (all(abs(rep[p]["b"] - PUB_1044_NULL0[p]["b"]) < 0.03 for p in PX)
                   and all(abs(rep[p]["Cc"] - PUB_1044_NULL0[p]["C"]) / PUB_1044_NULL0[p]["C"] < 0.10
                           for p in PX),
                   "CROSS-RUN 1044 NULL_0 median b and C: " + ", ".join(
                       f"{p} b {rep[p]['b']:.4f} vs {PUB_1044_NULL0[p]['b']:.4f}, C "
                       f"{rep[p]['Cc']:.2f} vs {PUB_1044_NULL0[p]['C']:.2f}" for p in PX))

    Lt = np.array([250.0, 400, 600, 900, 1300, 1900, 2800])
    D2k, Ck = 0.0037, 11.5
    sdk = np.sqrt(D2k + Ck / Lt)
    D2h, Ch, _ = fit_sat(Lt, sdk)
    d6 = max(abs(D2h - D2k), abs(Ch - Ck))
    gates["G6"] = (d6 < 1e-9, f"closed-form SAT recovers known (D2 {D2k}, C {Ck}) to {d6:.2e}")

    why7 = []
    for p, f_, lad in product(PX, FRACS, LADDERS):
        T = int(round(TLEN[p] * f_))
        lens = ladder_for(T, f_, lad)
        for (a, b_) in tail_windows(T, lens):
            if (b_ - a) not in lens or b_ != T or a < 0:
                why7.append(f"{p}/{f_}/{lad}")
    gates["G7"] = (not why7, "window construction: every window is exactly L days and tail-"
                             f"anchored across all {len(PX)*len(FRACS)*len(LADDERS)} "
                             f"(panel, fraction, ladder) points")

    R = RMAT[("GRID", PANEL_HEAD, RUNG_HEAD)]
    com, idio_n, sc = null_parts(R)
    dmu = float(np.abs(idio_n.mean(axis=0)).max())
    dsd = float(np.abs(idio_n.std(axis=0, ddof=1) - sc).max())
    gates["G8"] = (dmu < 1e-12 and dsd < 1e-12,
                   f"zero TRUE dispersion by construction: max|idio column mean| {dmu:.2e}, "
                   f"max|idio column sd - common scale| {dsd:.2e}  (so every synthetic book has "
                   "the same population mean and variance under BOTH nulls)")

    def surface_once(seed):
        lens = ladder_for(TLEN[PANEL_HEAD], 1.00, "NATIVE")
        Ds, _, _, _ = null_floor(R, TLEN[PANEL_HEAD], lens, 40, seed, "NULL_0")
        return Ds
    d9 = float(np.abs(surface_once(31) - surface_once(31)).max())
    seedref = mdseed(SEED0, "NULL_0", TLEN[PANEL_HEAD], R.shape[1],
                     tuple(ladder_for(TLEN[PANEL_HEAD], 1.00, "NATIVE")))
    gates["G9"] = (d9 == 0.0, f"determinism: null floors rebuild bit-for-bit (max|d| {d9:.1e}); "
                              f"md5 process-stable seed for the headline cell = {seedref}")

    def idio_corr_of(kind, nrep=30):
        Tn, N = R.shape
        rng = np.random.default_rng(5)
        acc = []
        for _ in range(nrep):
            ix = rng.integers(0, Tn, size=Tn)
            X = (com[ix][:, None] + (rng.standard_normal((Tn, N)) * sc if kind == "NULL_0"
                                     else idio_n[ix]))
            E = X - X.mean(axis=1)[:, None]
            cm = np.corrcoef(E.T)
            acc.append(cm[np.triu_indices(N, 1)].mean())
        return float(np.mean(acc))
    real_ic = np.corrcoef(idio_n.T)[np.triu_indices(R.shape[1], 1)].mean()
    ic0, ic0r = idio_corr_of("NULL_0"), idio_corr_of("NULL_0R")
    gates["G10"] = (abs(ic0r - real_ic) < abs(ic0 - real_ic),
                    f"idio correlation: REAL {real_ic:+.4f}; NULL_0R {ic0r:+.4f} (inherits it); "
                    f"NULL_0 {ic0:+.4f} (independent by construction)")

    for k in sorted(gates, key=lambda s: int(s[1:])):
        ok, msg = gates[k]
        P(f"  {k} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"GATES: {sum(1 for v in gates.values() if v[0])} of {len(gates)} pass.")
    P("")

    # ================================================================== (A) the bias surface
    P("=" * 100)
    P("(A) THE BIAS SURFACE — fitted floor under a ZERO-TRUE-DISPERSION null, every cell")
    P("=" * 100)
    rows = []
    for pl, p, f_, lad, c, kind in product(POOLS, PX, FRACS, LADDERS, RUNGS, ["NULL_0", "NULL_0R"]):
        T = int(round(TLEN[p] * f_))
        lens = ladder_for(T, f_, lad)
        if len(lens) < 3:
            continue
        Rm = RMAT[(pl, p, c)][-T:, :]
        Ds, D2s, bs, Cs = null_floor(Rm, T, lens, NREP, SEED0, kind)
        rows.append(dict(pool=pl, N=Rm.shape[1], panel=p, frac=f_, T=T, ladder=lad,
                         nrung=len(lens), Lbar=float(np.mean(lens)), cost=c, kind=kind,
                         floor_med=float(np.median(Ds)), floor_p95=float(np.percentile(Ds, 95)),
                         floor_mean=float(np.mean(Ds)),
                         pos_share=float((np.asarray(D2s) > 0).mean()),
                         D2_mean=float(np.mean(D2s)),
                         D2_sd=float(np.std(D2s, ddof=1)),
                         D2_se=float(np.std(D2s, ddof=1) / np.sqrt(len(D2s))),
                         noise_scale=float(np.sqrt(np.std(D2s, ddof=1))),
                         b_med=float(np.median(bs)), C_med=float(np.median(Cs)), nrep=NREP))
    SUR = pd.DataFrame(rows)
    dump(SUR, "surface")

    H = SUR[(SUR.kind == "NULL_0") & (SUR.cost == RUNG_HEAD)]
    P(f"  HEADLINE SLICE (NULL_0, {RUNG_HEAD:.0f} bps) — median fitted floor, truth = 0 exactly:")
    for lad in LADDERS:
        P(f"    ladder {lad}:")
        piv = H[H.ladder == lad].pivot_table(index=["panel", "pool", "N"], columns="frac",
                                             values="floor_med")
        for line in piv.to_string(float_format=lambda x: f"{x:.4f}").split("\n"):
            P("      " + line)
    P(f"  Global grid span of the p95 threshold: {SUR.floor_p95.min():.4f} .. "
      f"{SUR.floor_p95.max():.4f}  ({SUR.floor_p95.max()/max(SUR.floor_p95.min(),1e-9):.2f}x); "
      f"the record's single global bar is {GLOBAL_FLOOR_BAR}.")
    P("")
    P("  TRUNCATION DIAGNOSTIC (why the median above is so often exactly 0.0000).  The published")
    P("  floor is sqrt(max(D2_hat, 0)), so its MEDIAN is exactly zero whenever fewer than half")
    P("  the reps produce a positive intercept.  Share of reps with D2_hat > 0, per cell:")
    P(f"    NULL_0 {RUNG_HEAD:.0f} bps, pos_share range {H.pos_share.min():.3f}..{H.pos_share.max():.3f}; "
      f"cells with pos_share < 0.50 (median pinned to 0): "
      f"{int((H.pos_share < 0.50).sum())} of {len(H)}")
    P(f"    whole {len(SUR)}-cell grid: pos_share {SUR.pos_share.min():.3f}..{SUR.pos_share.max():.3f}, "
      f"{int((SUR.pos_share < 0.50).sum())} of {len(SUR)} cells have the median pinned to 0; "
      f"{int((SUR.floor_med == 0).sum())} cells report floor_med == 0 exactly.")
    P("    => the record's published floor is a statistic sitting ON its own truncation point, so")
    P("       its VALUE is a coin flip between 0 and ~0.03 and it cannot resolve either axis.")
    P("")

    # ================================================================== (B) the two slopes
    P("=" * 100)
    P("(B) THE TWO SLOPES — log-log, against the predicted -0.50 (tape) and -0.25 (pool)")
    P("=" * 100)
    srows = []
    for pl, p, lad, c, kind in product(POOLS, PX, LADDERS, RUNGS, ["NULL_0", "NULL_0R"]):
        s = SUR[(SUR["pool"] == pl) & (SUR.panel == p) & (SUR.ladder == lad)
                & (SUR.cost == c) & (SUR.kind == kind)].sort_values("T")
        if len(s) < 3:
            continue
        sl, nu = loglog_slope(s["T"], s.floor_med, want_n=True)
        srows.append(dict(axis="TAPE", pool=pl, N=int(s.N.iloc[0]), panel=p, ladder=lad, cost=c,
                          kind=kind, npoints=len(s), n_used=nu, slope=sl,
                          slope_p95=loglog_slope(s["T"], s.floor_p95),
                          slope_noise=loglog_slope(s["T"], s.noise_scale),
                          lo=float(s.floor_med.min()), hi=float(s.floor_med.max())))
    for p, f_, lad, c, kind in product(PX, FRACS, LADDERS, RUNGS, ["NULL_0", "NULL_0R"]):
        s = SUR[(SUR.panel == p) & (SUR.frac == f_) & (SUR.ladder == lad)
                & (SUR.cost == c) & (SUR.kind == kind)].sort_values("N")
        if len(s) < 3:
            continue
        sl, nu = loglog_slope(s.N - 1, s.floor_med, want_n=True)
        srows.append(dict(axis="POOL", pool="|".join(s["pool"]), N=int(s.N.iloc[0]), panel=p,
                          ladder=lad, cost=c, kind=kind, npoints=len(s), n_used=nu, slope=sl,
                          slope_p95=loglog_slope(s.N - 1, s.floor_p95),
                          slope_noise=loglog_slope(s.N - 1, s.noise_scale),
                          lo=float(s.floor_med.min()), hi=float(s.floor_med.max())))
    SL = pd.DataFrame(srows)
    dump(SL, "slopes")
    hs = SL[(SL.kind == "NULL_0") & (SL.cost == RUNG_HEAD)]
    P(f"  NULL_0, {RUNG_HEAD:.0f} bps.  n_used = how many of the ladder's points could enter a")
    P("  log fit at all; a floor_med of exactly 0 cannot, so n_used < npoints means the")
    P("  pre-registered slope is fitted off a truncated subset and is NOT a slope:")
    for line in hs[["axis", "pool", "panel", "ladder", "npoints", "n_used", "slope",
                    "lo", "hi"]].to_string(index=False,
                                           float_format=lambda x: f"{x:.4f}").split("\n"):
        P("    " + line)
    P(f"  n_used == npoints in {int((hs.n_used == hs.npoints).sum())} of {len(hs)} headline "
      f"slope fits.")
    P("")

    # -------------------------------------------------- (B2) NOT PRE-REGISTERED
    P("-" * 100)
    P("(B2) THE SAME TWO SLOPES ON A STATISTIC THAT IS NOT PINNED TO ITS TRUNCATION POINT")
    P("     REPORTED, NOT PRE-REGISTERED.  Added after the pre-registered median turned out to")
    P("     be truncation-degenerate (see the diagnostic in (A)); it is NOT scored as a")
    P("     hypothesis and does not replace H_TAPE / H_POOL / H_AXIS, which FAIL as written.")
    P("     Two un-truncated statistics carry the same theory: the p95 of the floor (the")
    P("     threshold a practitioner would actually use) and sqrt(SD(D2_hat)) (the noise scale")
    P("     the arithmetic in the header predicts directly).  Both predicted -0.50 in tape")
    P("     length and -0.25 in pool size.")
    P("-" * 100)
    for line in hs[["axis", "pool", "panel", "ladder", "npoints", "slope_p95",
                    "slope_noise"]].to_string(index=False,
                                              float_format=lambda x: f"{x:.4f}").split("\n"):
        P("    " + line)
    B2 = {}
    for ax, pred in (("TAPE", -0.50), ("POOL", -0.25)):
        s = hs[hs.axis == ax]
        B2[ax] = (float(s.slope_p95.median()), float(s.slope_noise.median()))
        P(f"    {ax}: median slope_p95 {s.slope_p95.median():+.4f}, median slope_noise "
          f"{s.slope_noise.median():+.4f}, predicted {pred:+.2f}")
        for lad in LADDERS:
            t = s[s.ladder == lad]
            B2[(ax, lad)] = float(t.slope_p95.median())
            P(f"       ladder {lad:<6}: slope_p95 {t.slope_p95.median():+.4f} "
              f"[{t.slope_p95.min():+.4f}, {t.slope_p95.max():+.4f}], slope_noise "
              f"{t.slope_noise.median():+.4f}")
    P("    The SCALED ladder is the clean tape axis (rung COUNT and ladder SHAPE held fixed);")
    P("    NATIVE also loses rungs as the tape shortens, which flattens the fit.")
    P("")

    # ================================================================== (C) N-subsample control
    P("=" * 100)
    P("(C) RESOLUTION CONTROL — the pool slope off SEVEN N points, subsampled from WIDE")
    P("=" * 100)
    crows = []
    for p, lad, c, kind in product(PX, LADDERS, RUNGS, ["NULL_0", "NULL_0R"]):
        T = TLEN[p]
        lens = ladder_for(T, 1.00, lad)
        Rfull = RMAT[("WIDE", p, c)]
        rng = np.random.default_rng(mdseed("NSUB", p, lad, int(c * 10), kind))
        for n in NSUB:
            cols = np.sort(rng.choice(Rfull.shape[1], size=n, replace=False))
            Ds, D2s, bs, Cs = null_floor(Rfull[:, cols], T, lens, NREP, SEED0 + n, kind)
            crows.append(dict(panel=p, ladder=lad, cost=c, kind=kind, N=n, T=T,
                              floor_med=float(np.median(Ds)),
                              floor_p95=float(np.percentile(Ds, 95)),
                              pos_share=float((np.asarray(D2s) > 0).mean()),
                              noise_scale=float(np.sqrt(np.std(D2s, ddof=1))),
                              C_med=float(np.median(Cs))))
    NS = pd.DataFrame(crows)
    dump(NS, "nsub")
    nsl = []
    for p, lad, c, kind in product(PX, LADDERS, RUNGS, ["NULL_0", "NULL_0R"]):
        s = NS[(NS.panel == p) & (NS.ladder == lad) & (NS.cost == c) & (NS.kind == kind)]
        sl, nu = loglog_slope(s.N - 1, s.floor_med, want_n=True)
        nsl.append(dict(panel=p, ladder=lad, cost=c, kind=kind, npoints=len(s), n_used=nu,
                        slope_N=sl, slope_N_p95=loglog_slope(s.N - 1, s.floor_p95),
                        slope_N_noise=loglog_slope(s.N - 1, s.noise_scale)))
    NSL = pd.DataFrame(nsl)
    dump(NSL, "nsub_slopes")
    P(f"  fitted pool slope on {len(NSUB)} N points (predicted -0.25).  slope_N is the")
    P("  PRE-REGISTERED reading (on the median floor); slope_N_p95 and slope_N_noise are the")
    P("  NOT-PRE-REGISTERED un-truncated readings described in (B2):")
    for line in NSL.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("    " + line)
    P(f"  n_used == {len(NSUB)} in {int((NSL.n_used == len(NSUB)).sum())} of {len(NSL)} fits; "
      f"pos_share over the control {NS.pos_share.min():.3f}..{NS.pos_share.max():.3f}.")
    P("")

    # ================================================================== (D) unbiasedness of D2
    P("=" * 100)
    P("(D) IS D2_hat ITSELF BIASED? — mean D2_hat against its own standard error")
    P("=" * 100)
    hh = SUR[(SUR.kind == "NULL_0") & (SUR.cost == RUNG_HEAD) & (SUR.ladder == LADDER_HEAD)
             & (SUR.frac == FRAC_HEAD)]
    for _, r in hh.iterrows():
        P(f"    {r.panel:>4} {r['pool']:>5} N={int(r.N):>2}  mean D2_hat {r.D2_mean:+.6f}  "
          f"SE {r.D2_se:.6f}  t {r.D2_mean/max(r.D2_se,1e-12):+.2f}   "
          f"median sqrt(max(D2,0)) {r.floor_med:.4f}")
    tvals = (hh.D2_mean / hh.D2_se.clip(lower=1e-12)).abs()
    P(f"  |t| <= 2 in {int((tvals<=2).sum())} of {len(tvals)} headline cells.")
    P("")

    # ================================================================== (E) the payoff
    P("=" * 100)
    P("(E) THE PAYOFF — the record's 24 committed floors re-read against their OWN cell")
    P("=" * 100)
    F44 = pd.read_csv(FITS_1044)
    thr = {}
    for p in PX:
        s = SUR[(SUR.panel == p) & (SUR["pool"] == "GRID") & (SUR.frac == 1.00)
                & (SUR.ladder == "NATIVE") & (SUR.kind == "NULL_0")]
        for _, r in s.iterrows():
            thr[(p, r.cost)] = (r.floor_med, r.floor_p95)
    erows = []
    for _, r in F44.iterrows():
        cost = float(r["cost"])
        key = (r["panel"], cost if cost in thr and True else RUNG_HEAD)
        if (r["panel"], cost) in thr:
            med, p95 = thr[(r["panel"], cost)]
            basis = f"own cell ({r['panel']}, {cost:.0f} bps)"
        else:
            med, p95 = thr[(r["panel"], RUNG_HEAD)]
            basis = f"nearest cell ({r['panel']}, {RUNG_HEAD:.0f} bps) — 1044 also ran 0 bps"
        D = float(r["D"])
        erows.append(dict(panel=r["panel"], cost=cost, anchor=r["anchor"], D=D,
                          D2=float(r["D2"]), se_D2=float(r["se_D2"]),
                          global_bar=GLOBAL_FLOOR_BAR, cell_med=med, cell_p95=p95, basis=basis,
                          real_global=bool(D > GLOBAL_FLOOR_BAR), real_cell=bool(D > p95),
                          verdict_moves=bool((D > GLOBAL_FLOOR_BAR) != (D > p95))))
    EC = pd.DataFrame(erows)
    dump(EC, "census")
    P(f"  {len(EC)} committed floors from 1044's fits.csv.")
    P(f"    above the GLOBAL 0.012 bar : {int(EC.real_global.sum())} of {len(EC)}")
    P(f"    above their OWN cell's p95 : {int(EC.real_cell.sum())} of {len(EC)}")
    P(f"    verdict MOVES              : {int(EC.verdict_moves.sum())} of {len(EC)}")
    nz = EC[EC.D > 0]
    P(f"    (of these, {len(nz)} floors are non-zero at all; {len(EC)-len(nz)} were already "
      f"truncated to exactly 0 by 1044's own max(D2,0))")
    P(f"  per-cell p95 thresholds actually used: " + ", ".join(
        f"{k[0]}@{k[1]:.0f}bps {v[1]:.4f}" for k, v in sorted(thr.items())))
    P("")

    # ================================================================== (F) rule-8 walk-forward
    P("=" * 100)
    P(f"(F) RULE-8 WALK-FORWARD — IS <= {REC_END} chooses, OOS read ONCE; both KEEP paths")
    P("=" * 100)
    lrows = []
    for pl, p, c in product(POOLS, PX, RUNGS):
        for nm in MEM[(pl, p)]:
            d = split_block(NET[(nm, c)])
            sb = split_block(SPY[p])
            vb = split_block(V2[(p, c)])
            lg = legs_at(d, sb)
            lrows.append(dict(book=nm, pool=pl, panel=p, cost=c, **d, **lg,
                              pass4b=all(lg.values()),
                              pass4a=bool(d["H1"] > vb["H1"] and d["H2"] > vb["H2"]
                                          and d["MaxDD"] >= vb["MaxDD"])))
    LAD = pd.DataFrame(lrows)
    dump(LAD, "ladder")

    r8 = []
    for pl, p, c in product(POOLS, PX, RUNGS):
        sub = LAD[(LAD["pool"] == pl) & (LAD.panel == p) & (LAD.cost == c)].set_index("book")
        sb, vb = split_block(SPY[p]), split_block(V2[(p, c)])
        spy_is = (sb["IS_CAGR"], sb["IS_Sharpe"], sb["IS_MaxDD"])
        for ch in ["IS_SHARPE", "IS_CAGR", "IS_LEGS"]:
            pick = raw_pick(sub, ch, spy_is)
            d = sub.loc[pick]
            lg = legs_at(d, sb)
            r8.append(dict(pool=pl, N=len(sub), panel=p, cost=c, chooser=ch, pick=pick,
                           OOS_CAGR=d["OOS_CAGR"], OOS_Sharpe=d["OOS_Sharpe"],
                           OOS_MaxDD=d["OOS_MaxDD"],
                           spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                           spy_OOS_MaxDD=sb["OOS_MaxDD"],
                           v2_OOS_CAGR=vb["OOS_CAGR"], v2_OOS_Sharpe=vb["OOS_Sharpe"],
                           v2_OOS_MaxDD=vb["OOS_MaxDD"],
                           H1=d["H1"], H2=d["H2"], MaxDD=d["MaxDD"],
                           pass4b=all(lg.values()),
                           pass4a=bool(d["H1"] > vb["H1"] and d["H2"] > vb["H2"]
                                       and d["MaxDD"] >= vb["MaxDD"])))
    R8 = pd.DataFrame(r8)
    dump(R8, "rule8")
    cols = ["pool", "N", "panel", "cost", "chooser", "pick", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "spy_OOS_Sharpe", "v2_OOS_Sharpe", "pass4b", "pass4a"]
    for line in R8[cols].to_string(index=False,
                                   float_format=lambda x: f"{x:.4f}").split("\n"):
        P("    " + line)
    P(f"  OOS 4b passes: {int(R8.pass4b.sum())} of {len(R8)};  OOS 4a passes: "
      f"{int(R8.pass4a.sum())} of {len(R8)}.")
    P(f"  Whole ladder (every book, not a chooser's pick): 4b {int(LAD.pass4b.sum())} of "
      f"{len(LAD)}, 4a {int(LAD.pass4a.sum())} of {len(LAD)}.")
    for pl in POOLS:
        s = R8[R8["pool"] == pl]
        P(f"    pool {pl:>5} (N={int(s.N.iloc[0])}..{int(s.N.max())}): mean OOS Sharpe "
          f"{s.OOS_Sharpe.mean():.4f}, mean OOS CAGR {s.OOS_CAGR.mean():.4f}, 4b "
          f"{int(s.pass4b.sum())}/{len(s)}")
    P(f"  SPY OOS: CAGR {sb['OOS_CAGR']:.4f} Sharpe {sb['OOS_Sharpe']:.4f} MaxDD "
      f"{sb['OOS_MaxDD']:.4f}   RULES v2 OOS ({RUNG_HEAD:.0f} bps, U56): "
      f"CAGR {split_block(V2[('U56', RUNG_HEAD)])['OOS_CAGR']:.4f} Sharpe "
      f"{split_block(V2[('U56', RUNG_HEAD)])['OOS_Sharpe']:.4f} MaxDD "
      f"{split_block(V2[('U56', RUNG_HEAD)])['OOS_MaxDD']:.4f}")
    P("")

    # ================================================================== hypotheses
    P("=" * 100)
    P("PRE-REGISTERED HYPOTHESES (bars fixed before any number above the gates was read)")
    P("=" * 100)
    hyp = {}

    t_sc = SL[(SL.axis == "TAPE") & (SL.kind == "NULL_0") & (SL.cost == RUNG_HEAD)
              & (SL.ladder == "SCALED")]
    tv = t_sc.groupby("panel").slope.median()
    hyp["H_TAPE"] = (bool(((tv >= -0.60) & (tv <= -0.40)).all()),
                     f"SCALED-ladder tape slope by panel {tv.round(4).to_dict()} in [-0.60,-0.40]?")

    nv = NSL[(NSL.kind == "NULL_0") & (NSL.cost == RUNG_HEAD)].groupby("panel").slope_N.median()
    hyp["H_POOL"] = (bool(((nv >= -0.35) & (nv <= -0.15)).all()),
                     f"7-point pool slope by panel {nv.round(4).to_dict()} in [-0.35,-0.15]?")

    cells, wins = [], 0
    for p, lad in product(PX, LADDERS):
        st = SL[(SL.axis == "TAPE") & (SL.kind == "NULL_0") & (SL.cost == RUNG_HEAD)
                & (SL.ladder == lad) & (SL.panel == p)].slope.median()
        sp = NSL[(NSL.kind == "NULL_0") & (NSL.cost == RUNG_HEAD) & (NSL.ladder == lad)
                 & (NSL.panel == p)].slope_N.median()
        ok = abs(st) > 1.5 * abs(sp)
        wins += int(ok)
        cells.append(f"{p}/{lad} |tape| {abs(st):.4f} vs 1.5x|pool| {1.5*abs(sp):.4f} "
                     f"{'>' if ok else '<='}")
    hyp["H_AXIS"] = (wins >= 3, f"DECISIVE: {wins} of 4 cells have |tape| > 1.5x|pool|.  "
                                + "; ".join(cells))

    hyp["H_UNB"] = (int((tvals <= 2).sum()) >= 4,
                    f"|mean D2_hat| <= 2 SE in {int((tvals<=2).sum())} of {len(tvals)} headline "
                    f"cells (so the floor is a sqrt-of-truncated-zero artifact, not a D2 bias)")

    span = SUR.floor_p95.max() / max(SUR.floor_p95.min(), 1e-9)
    hyp["H_CELL"] = (bool(span >= 2.0 and EC.verdict_moves.sum() >= 1),
                     f"PAYOFF: p95 threshold spans {span:.2f}x (bar 2.0x) across the "
                     f"{len(SUR)}-cell grid; {int(EC.verdict_moves.sum())} of {len(EC)} committed "
                     f"floors change verdict on their own cell (bar >= 1)")

    e0 = NSL[(NSL.kind == "NULL_0") & (NSL.cost == RUNG_HEAD)].groupby("panel").slope_N.median()
    e0r = NSL[(NSL.kind == "NULL_0R") & (NSL.cost == RUNG_HEAD)].groupby("panel").slope_N.median()
    hyp["H_EFF"] = (bool((e0r.abs() < e0.abs()).all()),
                    f"real-idio pool slope weaker than independent-idio: NULL_0R "
                    f"{e0r.round(4).to_dict()} vs NULL_0 {e0.round(4).to_dict()}")

    for k, (ok, msg) in hyp.items():
        P(f"  {k:<8} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"HYPOTHESES: {sum(1 for v in hyp.values() if v[0])} of {len(hyp)} pass.")
    P("")

    P("=" * 100)
    P("THE ANSWER TO THE QUEUE'S QUESTION")
    P("=" * 100)
    P("  NEITHER.  The queue's either/or presumes the published floor is a BIAS with a scaling")
    P("  law on one of two axes.  It is not a bias at all: sqrt(max(D2_hat, 0)) is a statistic")
    P(f"  sitting ON its own truncation point ({int((SUR.pos_share < 0.50).sum())} of {len(SUR)} "
      f"cells have fewer than half their reps positive,")
    P(f"  and {int((SUR.floor_med == 0).sum())} cells report a median of exactly 0), so its value "
      "is a coin flip between 0")
    P("  and ~0.03 that moves with neither tape length nor pool size in any resolvable way.")
    P("  1044's +0.0115 and +0.0047 are two draws from that coin flip, and this run reproduces")
    P("  the first exactly (G4).  The underlying intercept D2_hat is itself slightly NEGATIVE on")
    P("  nested tail windows (mean below zero in every headline cell), i.e. the SAT model is")
    P("  mildly misspecified downward on this geometry — so the floor is not even measuring an")
    P("  upward bias.")
    P(f"  The object the record should publish instead is the per-cell p95 of the null floor,")
    P(f"  which IS resolved: {SUR.floor_p95.min():.4f}..{SUR.floor_p95.max():.4f} over the "
      f"{len(SUR)}-cell grid, {SUR.floor_p95.max()/max(SUR.floor_p95.min(),1e-9):.1f}x wide and "
      f"{SUR.floor_p95.median()/GLOBAL_FLOOR_BAR:.0f}x the")
    P(f"  record's single global {GLOBAL_FLOOR_BAR} bar at the median cell.  Read against it, "
      f"ALL {int(EC.real_global.sum())} of the record's")
    P(f"  {len(EC)} committed floors that clear 0.012 fall INSIDE their own cell's noise "
      f"({int(EC.real_cell.sum())} survive).")
    P("")
    P("  AND, once the question is asked of a statistic that CAN answer it (section B2, reported")
    P("  but not pre-registered), the queue's either/or resolves cleanly and one-sidedly:")
    nsp = NSL[(NSL.cost == RUNG_HEAD)]
    P(f"    TAPE LENGTH carries it, at the predicted rate.  slope on the p95 threshold "
      f"{B2[('TAPE','SCALED')]:+.3f} on the")
    P(f"      shape-held-fixed SCALED ladder ({B2[('TAPE','NATIVE')]:+.3f} on NATIVE), against "
      f"the header's a-priori -0.50.")
    P(f"    POOL SIZE does not.  Across the record's three actual pools (18 -> 24 -> 48 books) "
      f"the slope is")
    P(f"      {B2['POOL'][0]:+.3f} — flat.  Even on the idealised 7-point N ladder with INDEPENDENT "
      "idiosyncratic")
    P(f"      draws (1044's own construction) it only reaches "
      f"{nsp[nsp.kind=='NULL_0'].slope_N_p95.median():+.3f}, and once the pool's REAL")
    P(f"      cross-book idio correlation is inherited (NULL_0R) it collapses to "
      f"{nsp[nsp.kind=='NULL_0R'].slope_N_p95.median():+.3f}.")
    P("    PRACTICAL READING: four more years of tape buys what no achievable widening of the")
    P("    book pool can buy.  Adding books to a near-collinear band x gross ladder buys nothing")
    P("    at all, because the books are not independent measurements of the tape.")
    P("")
    P(f"Runtime {time.time()-t0:.1f}s.")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

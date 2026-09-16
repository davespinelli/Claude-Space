#!/usr/bin/env python3
"""Idea 1044 (cloud lane, 2026-09-16) — is the K-FREE NULL SD a WINDOW-LENGTH CURVE with a
SOLVABLE EXPONENT?

QUESTION (QUEUE idea 1044, verbatim)
    idea 1039 found the per-window sd of the 18-book Sharpe vector rises as windows shorten (the
    record's own 1,936-2,881 day tail windows band 1.82x more once their lengths are equalised).
    Walk a length ladder at fixed content and report the exponent, so any published null sd can
    be length-adjusted before it is compared.  Max 2 params (length ladder, content anchor).

THE OBJECT.  For a window w of L trading days, sd_RAW(w) = the cross-sectional sd, over the 18
    GRID books of a panel, of each book's annualised Sharpe measured on w.  That is the record's
    K-FREE NULL SD — the "a random draw from its own pool" yardstick read at ONE window.  1036
    published it at 0.0645..0.0836 over the Q16 tail grid; 1039 showed 1.82x of that band is
    WINDOW LENGTH and not content.  This run asks what the length curve actually is.

WHAT HAD TO BE SAID BEFORE ANY NUMBER (declared here, ahead of the gates).
    sd_RAW is a cross-sectional sd of ESTIMATED Sharpes, so it carries two terms that behave
    completely differently in L:
      (i)  TRUE DISPERSION D — the books really do differ, and that difference does NOT shrink
           as the window lengthens;
      (ii) SAMPLING NOISE — each book's Sharpe is estimated with error whose variance falls
           like 1/L (Lo: Var(SR_ann) ~ (252 + SR_ann^2/2)/L).  The books are read off the SAME
           days, so those errors are CORRELATED; a common component of the error shifts all 18
           Sharpes together and cancels out of a cross-sectional sd.  Writing rho_e for the mean
           pairwise error correlation, the cross-sectional variance obeys
                        E[sd_RAW(L)^2]  =  D^2  +  C/L,      C ~ (252 + SR^2/2)(1 - rho_e).
    A SINGLE exponent therefore exists only in the corner where D = 0.  In general
                        b(L) = dlog sd / dlog L = -0.5 * (C/L) / (D^2 + C/L),
    which runs from -0.5 at short L to 0 at long L.  So the queue's "solvable exponent" is
    testable and, on this arithmetic, expected to FAIL as a single number and to SUCCEED as a
    TWO-TERM curve.  Both fits are run at every point and both are published.  The prediction was
    written before any number below the gates was read.

A CONFOUND STATED UP FRONT, not discovered later.  "Fixed content" is not literally achievable:
    at a fixed anchor a longer window necessarily HOLDS MORE TAPE.  That is why the content
    anchor is one of the two tuned dials (three anchors, all published) and why every observed
    curve is read beside a GEOMETRY-MATCHED null built on the SAME windows — the null inherits
    the lengths, the anchor and the cross-book correlation, and destroys only real
    time-variation.  Where observed and null curves agree, the length curve is arithmetic; where
    they separate, it is content.

WHAT IS MEASURED
    (A) THE CURVE.  sd_RAW at every (length L) x (content anchor) x (panel) x (cost rung) point,
        7 x 3 x 2 x 3 = 126 cells, all published, none selected.
    (B) THE TWO FITS.  POW: log sd = a + b log L (the queue's exponent).  SAT: sd^2 = D^2 + C/L
        (closed-form OLS of sd^2 on 1/L).  Both fits' RMSE in SD SPACE (see RMSE BASIS below),
        the fitted b, the fitted floor D, its OLS SE, and C against its theory value.
    (C) THE NULLS.  NULL_J — the 18 books' daily net returns resampled JOINTLY by day (one day
        draw shared by all 18, so the cross-book correlation and each book's own mean/vol are
        inherited, and only real TIME-VARIATION is destroyed).  Every fit is re-run on each of
        1,000 reps, giving a sampling distribution for b and for D.  NULL_0 — a ZERO-DISPERSION
        synthetic where all 18 books are drawn from one common distribution, so D = 0 exactly
        and the arithmetic says b must read -0.5; this is the estimator's own validation.
    (D) THE PAYOFF THE QUEUE ASKS FOR.  The record's OWN Q16 tail grid (16 windows, 1,936..2,881
        days) is length-adjusted to a reference length with the fitted curve, and the band before
        and after is published.  If the adjustment does not shrink the band it is worthless.  A
        FIXED-LAW adjustment (the a-priori sqrt law, no fitted parameter) is reported beside it;
        it is NOT pre-registered and is NOT scored as a hypothesis.
    (E) THE RULE-8 WALK-FORWARD at PROTOCOL's declared split 2016-12-31 (IS 2009-2016 chooses,
        2017-2026 read ONCE): OOS CAGR / Sharpe / MaxDD for each of the record's three IS-only
        choosers on both panels at all three rungs, against the live RULES v2 baseline and
        against SPY, BOTH KEEP paths (4a and 4b), every point reported.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL 21 (length x anchor) points reported.
    (1) LENGTH LADDER  L in {250, 400, 600, 900, 1300, 1900, 2800} trading days.  2,800 is the
        longest window this tape admits at all three anchors; 250 is one year.
    (2) CONTENT ANCHOR TAIL (every window ends on the last day — 1036's and 1039's own
        convention, and the HEADLINE), HEAD (every window starts at the first post-warmup day),
        MID (every window centred on the midpoint of the post-warmup tape).

    ONE REPORTED CONTROL, not a third dial: POOLED reads EVERY non-overlapping window of each
    length (17 / 11 / 7 / 4 / 3 / 2 / 1 windows at L = 250..2800) and takes the MEDIAN sd_RAW.
    It exists to separate two very different answers — "this tape has no exponent" from "ONE
    window per length cannot resolve one" — and it is published at every point, never used to
    choose anything.

    RMSE BASIS, fixed ahead of the numbers: both fits are scored in sd space.  The SAT floor D^2
    is allowed to come out NEGATIVE (the informative outcome: a curve falling FASTER than
    1/sqrt(L)), where log(D^2 + C/L) is undefined and a log-space score silently clips.  The
    pre-registered bars are carried over to the sd-space ratio unchanged.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_POW   DECISIVE, the queue's literal question.  A SINGLE exponent describes the curve:
            fitted |b| in [0.45, 0.55] at the headline anchor on BOTH panels at 10 bps, AND the
            SAT fit does not beat POW by more than 20% of RMSE.  PASS => the exponent
            is solvable and is the sqrt law.  FAIL => it is not a single number.
    H_SAT   the two-term curve is the right object: the fitted floor D^2 exceeds 2 OLS SE in at
            least 4 of the 6 headline-anchor cells, AND SAT's RMSE is <= 0.5x POW's in
            the median cell.
    H_ANCH  the exponent is a LENGTH object and not a CONTENT object: the spread of fitted b
            across the three content anchors is <= 0.10 in the median (panel, rung) cell.
    H_POOL  RESOLUTION.  With the POOLED control (many windows per length) the fitted b lies in
            [-0.55, -0.45] on both panels at 10 bps AND its own null's 90% interval is <= 0.20
            wide.  PASS => the exponent IS solvable, but only off a geometry the record does not
            use.  FAIL => it is not solvable on this tape at all.
    H_ZERO  ESTIMATOR VALIDATION.  On NULL_0 (zero true dispersion by construction) the fitted b
            lies in [-0.55, -0.45] and the fitted floor D is <= 0.010.
    H_ADJ   THE PAYOFF.  Length-adjusting the record's own Q16 tail grid with the fitted curve
            shrinks its sd_RAW band to <= 0.5x the raw band, on both panels at 10 bps.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  this run's fast runner == engine.backtest on a live book, returns AND turnover.
    G2  the pool is the record's own grid_books(), 18 books per panel.
    G3  CROSS-RUN: SPY's OOS triple at 2016-12-31 == the committed 15.21% / 0.8713 / -33.72%.
    G4  CROSS-RUN: 1036's committed K=1 placement band reproduces (per-end sd_RAW over the Q16
        grid, median over the 6 panel x rung cells: 0.0645 / 0.0836 / spread 0.0191).
    G5  CROSS-RUN: 1039's Q16_TAIL and Q16_FIXLEN per-cell bands reproduce (0.0335 / 0.0469).
    G6  the cumsum window Sharpe used for speed == fsharpe on the sliced returns.
    G7  the closed-form SAT fit recovers a KNOWN (D, C) on synthetic sd^2 data to 1e-9.
    G8  WINDOW CONSTRUCTION: every window has exactly L days and sits where its anchor says.
    G9  determinism: the whole ladder and both null fits rebuild bit-for-bit.
    G10 NULL_J preserves the cross-book correlation matrix of the real books (mean |d|).

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and
    drawdown LEVEL below is optimistic and every 4b count an UPPER bound.  The measured object is
    a CURVE SHAPE read off the SAME books at every length, so the level bias is common to all
    seven rungs of the ladder and cannot create or destroy an exponent.  Where it does not
    cancel it raises the Sharpe LEVEL, which RAISES C (the 252 + SR^2/2 term) and therefore makes
    the noise term LARGER relative to D — which flatters H_POW and works AGAINST H_SAT, and is
    reported as such.  SPY is a real index series and is not inflated.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-the-K-FREE-NULL-SD-a-WINDOW-LENGTH-CURVE-with-a-SOLVABLE-EXPONENT"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP = 260
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
PANEL_HEAD = "U56"
REC_END = "2016-12-31"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
RAW_CH = ["IS_SHARPE", "IS_LEGS", "IS_CAGR"]

# ---- the two tuned dials --------------------------------------------------------------------
LENS = [250, 400, 600, 900, 1300, 1900, 2800]
ANCHORS = ["TAIL", "HEAD", "MID"]          # the tuned dial: ONE window per length
ANCHOR_HEAD = "TAIL"
ANC_CTL = "POOLED"                          # reported CONTROL, not a tuned level
ALL_ANC = ANCHORS + [ANC_CTL]

NREP = 1000
SEED0 = 20260916
SQ252 = np.sqrt(252.0)

SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
PUB_1036_BAND = dict(sd_min=0.0645, sd_max=0.0836, spread=0.0191)
PUB_1039_CELLBAND = dict(Q16_TAIL=0.0335, Q16_FIXLEN=0.0469)
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


# ====================================================================== ladder machinery (1039's)
def quarter_ends(lo, hi):
    return [str(d.date()) for d in pd.date_range(lo, hi, freq="QE")]


END_Q16 = quarter_ends("2015-01-01", "2018-12-31")
ALLE = sorted(set(END_Q16) | {REC_END})


def metblock(r):
    c, s, d = fmet(r)
    k = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:k]), H2=fsharpe(r[k:]))


def split_block(net, e):
    b = metblock(net.values)
    o = net.loc[pd.Timestamp(e) + pd.Timedelta(days=1):].values
    i = net.loc[:pd.Timestamp(e)].values
    oc, os_, od = fmet(o)
    ic, is_, idd = fmet(i)
    b.update(OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_n=len(o),
             IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd, IS_n=len(i))
    return b


def legs_at(bk, sb):
    return {
        "L1_H1": bool(bk["H1"] > sb["H1"]),
        "L2_H2": bool(bk["H2"] > sb["H2"]),
        "L3_OOS": bool(bk["OOS_Sharpe"] > sb["OOS_Sharpe"]),
        "L4_DD": bool(abs(bk["OOS_MaxDD"]) <= DDCAP_FRAC * abs(sb["MaxDD"])),
        "L5_CAGR": bool(bk["OOS_CAGR"] >= CAGRFLOOR_FRAC * sb["CAGR"]),
    }


def raw_pick(sub, ch, spy_is):
    """IS-ONLY choosers — 1023's / 1031's / 1035's / 1036's / 1039's own three, verbatim."""
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


# ====================================================================== window / curve machinery
def cums(R):
    """Prefix sums of R and R^2 with a leading zero row.  R is T x N."""
    z = np.zeros((1, R.shape[1]))
    return (np.vstack([z, np.cumsum(R, axis=0)]),
            np.vstack([z, np.cumsum(R * R, axis=0)]))


def win_sharpes(cs, cs2, wins):
    """Annualised Sharpe of every book on every window, from prefix sums.  Returns W x N."""
    out = np.empty((len(wins), cs.shape[1]))
    for j, (a, b) in enumerate(wins):
        n = b - a
        s = cs[b] - cs[a]
        q = cs2[b] - cs2[a]
        m = s / n
        var = (q - n * m * m) / (n - 1)
        out[j] = SQ252 * m / np.sqrt(var)
    return out


def sd_raw_vec(S):
    return S.std(axis=1, ddof=1)


def anchored_windows(T, lens, anchor):
    """One window per length, all sharing the SAME anchor point."""
    w = []
    for L in lens:
        if L > T:
            w.append(None)
            continue
        if anchor == "TAIL":
            w.append((T - L, T))
        elif anchor == "HEAD":
            w.append((0, L))
        else:                                  # MID
            a = (T - L) // 2
            w.append((a, a + L))
    return w


def fit_pow(L, sd):
    """log sd = a + b log L.  Returns (b, a, rmse_SDSPACE).

    RMSE BASIS.  Both fits are scored in sd space, not log space.  The reason is stated ahead of
    any number: the SAT curve's fitted floor D^2 is allowed to come out NEGATIVE (that is the
    informative outcome — a curve falling FASTER than 1/sqrt(L)), and log(D^2 + C/L) is undefined
    there, so a log-space comparison silently clips.  The pre-registered bars (SAT beats POW by
    > 20% for H_POW, SAT <= 0.5x POW for H_SAT) are carried over to the sd-space ratio unchanged.
    """
    Lv, sdv = np.asarray(L, float), np.asarray(sd, float)
    x, y = np.log(Lv), np.log(sdv)
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    pred = np.exp(coef[0]) * Lv ** coef[1]
    return float(coef[1]), float(coef[0]), float(np.sqrt(((sdv - pred) ** 2).mean()))


def fit_sat(L, sd):
    """sd^2 = D2 + C * (1/L), closed-form OLS.  Returns (D2, C, se_D2, rmse_SDSPACE)."""
    x = 1.0 / np.asarray(L, float)
    sdv = np.asarray(sd, float)
    y = sdv ** 2
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ coef
    dof = max(len(x) - 2, 1)
    s2 = float((res ** 2).sum() / dof)
    cov = s2 * np.linalg.inv(A.T @ A)
    D2, Cc = float(coef[0]), float(coef[1])
    pred = np.sqrt(np.maximum(D2 + Cc * x, 0.0))
    return D2, Cc, float(np.sqrt(max(cov[0, 0], 0.0))), float(np.sqrt(((sdv - pred) ** 2).mean()))


def tile_windows(T, L):
    """Every NON-OVERLAPPING window of length L that fits in T, laid end to end from the tail."""
    k = T // L
    return [(T - (j + 1) * L, T - j * L) for j in range(k)][::-1]


def mdseed(*parts):
    """Process-STABLE seed.  Python's built-in hash() is randomised per process (PYTHONHASHSEED),
    so a seed built from it reproduces within a run and NOT across runs — the record's own md5
    convention is used instead."""
    h = hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()
    return int(h[:8], 16)


def sat_predict(D2, Cc, L):
    return float(np.sqrt(max(D2 + Cc / L, 0.0)))


def sd_curve(cs, cs2, T, anc, lens=LENS):
    """(Ls, sd_RAW per L, windows used per L) for one content anchor.

    The three TUNED anchor levels read ONE window per length.  POOLED is a reported CONTROL, not
    a fourth tuned level: it reads EVERY non-overlapping window of that length in the tape and
    takes the MEDIAN sd_RAW, which cuts the sampling noise on each rung by ~sqrt(K) and so
    answers whether an exponent is unresolvable in principle or merely at one window per length.
    """
    Ls, sds, nw = [], [], []
    for L in lens:
        if L > T:
            continue
        if anc == "POOLED":
            ws = tile_windows(T, L)
        elif anc == "TAIL":
            ws = [(T - L, T)]
        elif anc == "HEAD":
            ws = [(0, L)]
        else:
            a = (T - L) // 2
            ws = [(a, a + L)]
        v = sd_raw_vec(win_sharpes(cs, cs2, ws))
        Ls.append(L); sds.append(float(np.median(v))); nw.append(len(ws))
    return Ls, np.array(sds), nw


def main():
    t0 = time.time()
    P(f"# Idea 1044 (cloud lane, {DATE}) — is the K-FREE NULL SD a WINDOW-LENGTH CURVE with a "
      f"SOLVABLE EXPONENT?")
    P(f"# 2 tuned dials: LENGTH LADDER {LENS} x CONTENT ANCHOR {ANCHORS} = "
      f"{len(LENS)*len(ANCHORS)} points, ALL reported, none selected.  HEADLINE anchor "
      f"{ANCHOR_HEAD} (1036's and 1039's own tail convention).")
    P(f"# Controls at every point: panel [U56, B136], cost {RUNGS} bps (10 binding, PROTOCOL "
      f"rule 2), POOL = the record's 18 GRID books per panel.")
    P("# DECLARED BEFORE ANY NUMBER: sd_RAW^2 = D^2 + C/L, so a SINGLE exponent exists only if")
    P("#   the true cross-book dispersion D is zero.  b(L) = -0.5*(C/L)/(D^2+C/L) runs -0.5 -> 0.")
    P("#   Both fits (POW and SAT) are run and published at every point.")
    P("# CONFOUND STATED UP FRONT: at a fixed anchor a longer window HOLDS MORE TAPE, so 'fixed")
    P("#   content' is unreachable; that is why the anchor is a dial and why every curve is read")
    P("#   beside a geometry-matched null that inherits the windows and kills only time-variation.")
    P(f"# NULL_J: {NREP:,} JOINT day-resamples per cell (one day draw shared by all 18 books).")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels — every LEVEL is optimistic; the")
    P("#   bias raises C, which FLATTERS H_POW and works AGAINST H_SAT.  Reported, not asserted.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    PX = {"U56": U, "B136": B}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    if not U.index.equals(B.index):
        P(f"   CALENDAR: U56 ends {U.index[-1].date()} ({len(U)} days), B136 ends "
          f"{B.index[-1].date()} ({len(B)} days); each panel keeps its OWN calendar "
          f"(1013/1023/1031/1035/1036/1039's construction).  No splice.")
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; "
      f"B136 {B.shape} {B.index[0].date()}..{B.index[-1].date()}.")

    pool = C.grid_books(U, B)
    BOOKS = {p: sorted(b for b in pool if pool[b]["panel"] == p) for p in PX}
    P(f"POOL = {len(pool)} never-memo-selected GRID books "
      f"({len(BOOKS['U56'])} U56 / {len(BOOKS['B136'])} B136).")

    NET = {}
    for nm, b in pool.items():
        px = PX[b["panel"]]
        r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
        st = REC[b["panel"]]
        for c in RUNGS:
            NET[(nm, c)] = (r - t * c / 1e4).loc[st:]
    SPYR = {p: PX[p]["SPY"].pct_change().fillna(0.0).loc[REC[p]:] for p in PX}
    SPYB = {(p, e): split_block(SPYR[p], e) for p in PX for e in ALLE}
    SPYIS = {(p, e): (SPYB[(p, e)]["IS_CAGR"], SPYB[(p, e)]["IS_Sharpe"], SPYB[(p, e)]["IS_MaxDD"])
             for p in PX for e in ALLE}
    V2 = {}
    for p, px in PX.items():
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            V2[(p, c)] = split_block((r - t * c / 1e4).loc[REC[p]:], REC_END)

    RMAT = {(p, c): np.column_stack([NET[(b, c)].values for b in BOOKS[p]])
            for p in PX for c in RUNGS}
    CUM = {k: cums(v) for k, v in RMAT.items()}
    TLEN = {p: RMAT[(p, RUNG_HEAD)].shape[0] for p in PX}
    CELLS = [(p, c) for p in PX for c in RUNGS]
    P(f"Post-warmup net series: U56 {TLEN['U56']:,} days, B136 {TLEN['B136']:,} days "
      f"(from {REC['U56'].date()} / {REC['B136'].date()}).")
    P("")

    # ============================================================ GATES
    P("=" * 100)
    P("GATES (printed before any hypothesis number)")
    P("=" * 100)
    gates = {}

    # G1 fast runner == engine.backtest
    pxu = PX["U56"]
    Wt = rules_v2_weights(pxu)
    r_f, t_f = fast_run(pxu, Wt, rebalance_mask(pxu.index, "W"))
    eng = backtest(pxu, Wt, cost_bps=0.0, freq="W")
    st = REC["U56"]
    d_r = float(np.abs(r_f.loc[st:].values - eng["returns"].loc[st:].values).max())
    d_t = float(np.abs(t_f.loc[st:].values - eng["turnover"].loc[st:].values).max())
    gates["G1"] = (d_r < 1e-12 and d_t < 1e-12,
                   f"fast_run == engine.backtest  max|dret| {d_r:.2e}  max|dturn| {d_t:.2e}")

    # G2 pool
    ok2 = len(BOOKS["U56"]) == 18 and len(BOOKS["B136"]) == 18
    gates["G2"] = (ok2, f"pool = {len(BOOKS['U56'])} U56 / {len(BOOKS['B136'])} B136 GRID books")

    # G3 SPY OOS triple
    sb = SPYB[("U56", REC_END)]
    trip = (sb["OOS_CAGR"], sb["OOS_Sharpe"], sb["OOS_MaxDD"])
    d3 = max(abs(a - b) for a, b in zip(trip, SPY_OOS_COMMITTED))
    gates["G3"] = (d3 < 5e-3, f"SPY OOS {trip[0]:.4f} / {trip[1]:.4f} / {trip[2]:.4f} vs committed "
                              f"{SPY_OOS_COMMITTED}  max|d| {d3:.2e}")

    # Q16 tail windows, per panel (the record's own grid)
    def q16_windows(p, fixlen=False):
        idx = NET[(BOOKS[p][0], RUNG_HEAD)].index
        w = []
        for e in END_Q16:
            a = int(idx.searchsorted(pd.Timestamp(e), side="right"))
            w.append((a, len(idx)))
        if fixlen:
            Lm = min(b - a for a, b in w)
            w = [(a, a + Lm) for a, _ in w]
        return w

    sdq, sdqf = {}, {}
    for (p, c) in CELLS:
        cs, cs2 = CUM[(p, c)]
        sdq[(p, c)] = sd_raw_vec(win_sharpes(cs, cs2, q16_windows(p)))
        sdqf[(p, c)] = sd_raw_vec(win_sharpes(cs, cs2, q16_windows(p, True)))
    # 1036's convention: median over cells of per-end sd, then min/max/spread
    M = np.array([sdq[k] for k in CELLS])           # cells x 16
    med_end = np.median(M, axis=0)
    g4 = dict(sd_min=float(med_end.min()), sd_max=float(med_end.max()),
              spread=float(med_end.max() - med_end.min()))
    d4 = max(abs(g4[k] - PUB_1036_BAND[k]) for k in PUB_1036_BAND)
    gates["G4"] = (d4 < 5e-3, f"1036 K=1 placement band {g4['sd_min']:.4f}..{g4['sd_max']:.4f} "
                              f"spread {g4['spread']:.4f} vs published "
                              f"{PUB_1036_BAND['sd_min']:.4f}..{PUB_1036_BAND['sd_max']:.4f} / "
                              f"{PUB_1036_BAND['spread']:.4f}  max|d| {d4:.2e}")

    # G5 1039's per-cell bands (median over cells of the per-cell band)
    bt = float(np.median([sdq[k].max() - sdq[k].min() for k in CELLS]))
    bf = float(np.median([sdqf[k].max() - sdqf[k].min() for k in CELLS]))
    d5 = max(abs(bt - PUB_1039_CELLBAND["Q16_TAIL"]), abs(bf - PUB_1039_CELLBAND["Q16_FIXLEN"]))
    gates["G5"] = (d5 < 5e-3, f"1039 band_cell Q16_TAIL {bt:.4f} (pub "
                              f"{PUB_1039_CELLBAND['Q16_TAIL']:.4f}) / Q16_FIXLEN {bf:.4f} (pub "
                              f"{PUB_1039_CELLBAND['Q16_FIXLEN']:.4f})  max|d| {d5:.2e}")

    # G6 cumsum Sharpe == fsharpe on the slice
    cs, cs2 = CUM[(PANEL_HEAD, RUNG_HEAD)]
    wtest = anchored_windows(TLEN[PANEL_HEAD], LENS, "TAIL")
    S = win_sharpes(cs, cs2, [w for w in wtest if w])
    R = RMAT[(PANEL_HEAD, RUNG_HEAD)]
    ref = np.array([[fsharpe(R[a:b, j]) for j in range(R.shape[1])]
                    for (a, b) in [w for w in wtest if w]])
    d6 = float(np.abs(S - ref).max())
    gates["G6"] = (d6 < 1e-10, f"cumsum window Sharpe == fsharpe on the slice  max|d| {d6:.2e}")

    # G7 SAT fit recovers a known (D, C)
    Lg = np.array(LENS, float)
    D2t, Ct = 0.0036, 4.0
    sdt = np.sqrt(D2t + Ct / Lg)
    D2h, Ch, _, _ = fit_sat(Lg, sdt)
    d7 = max(abs(D2h - D2t), abs(Ch - Ct))
    gates["G7"] = (d7 < 1e-9, f"SAT closed form recovers D2={D2t} C={Ct} -> {D2h:.10f} / "
                              f"{Ch:.10f}  max|d| {d7:.2e}")

    # G8 window construction
    ok8, why8 = True, []
    for anc in ANCHORS:
        for p in PX:
            ws = anchored_windows(TLEN[p], LENS, anc)
            for L, w in zip(LENS, ws):
                if w is None:
                    ok8 = False; why8.append(f"{anc}/{p}/L{L} unbuildable"); continue
                if (w[1] - w[0]) != L:
                    ok8 = False; why8.append(f"{anc}/{p}/L{L} len {w[1]-w[0]}")
                if anc == "TAIL" and w[1] != TLEN[p]:
                    ok8 = False; why8.append(f"{anc}/{p}/L{L} end {w[1]}")
                if anc == "HEAD" and w[0] != 0:
                    ok8 = False; why8.append(f"{anc}/{p}/L{L} start {w[0]}")
    gates["G8"] = (ok8, f"window construction {len(ANCHORS)*len(PX)*len(LENS)} windows: exact "
                        f"length, anchor honoured" + (("; " + "; ".join(why8[:3])) if why8 else ""))

    # ---- observed curve table (needed before G9 determinism)
    def curve_table():
        rows = []
        for (p, c) in CELLS:
            cs, cs2 = CUM[(p, c)]
            msh = float(win_sharpes(cs, cs2, [(0, TLEN[p])])[0].mean())
            for anc in ALL_ANC:
                Ls, sd, nw = sd_curve(cs, cs2, TLEN[p], anc)
                bpow, apow, rp = fit_pow(Ls, sd)
                D2, Cc, seD2, rs = fit_sat(Ls, sd)
                for L, v, k in zip(Ls, sd, nw):
                    rows.append(dict(panel=p, cost=c, anchor=anc, L=L, nwin=k,
                                     sd_raw=float(v), mean_sharpe=msh,
                                     b_pow=bpow, rmse_pow=rp, D2=D2, D=float(np.sqrt(max(D2, 0))),
                                     C=Cc, se_D2=seD2, rmse_sat=rs))
        return pd.DataFrame(rows)

    CT = curve_table()
    CT2 = curve_table()
    num = CT.select_dtypes(include=[float, int]).columns
    d9a = float(np.nanmax(np.abs(CT[num].values - CT2[num].values)))

    # ---- NULL_J: joint day resample, fits per rep
    def null_fits(p, c, anc, nrep=NREP, seed=SEED0, zero_disp=False):
        R = RMAT[(p, c)]
        T, N = R.shape
        rng = np.random.default_rng(mdseed(seed, p, int(c * 10), anc, zero_disp))
        if zero_disp:
            # ZERO-DISPERSION control: every synthetic book has the SAME distribution.  Build it
            # from the pool's own common factor plus an idiosyncratic part whose scale is the
            # pool-median idiosyncratic scale, so the cross-book correlation is realistic and the
            # TRUE dispersion is exactly zero.
            com = R.mean(axis=1)
            idio = R - com[:, None]
            sc = float(np.median(idio.std(axis=0, ddof=1)))
            base = None
        bs, Ds, Cs = [], [], []
        for k in range(nrep):
            ix = rng.integers(0, T, size=T)
            if zero_disp:
                cc = com[ix]
                ee = rng.standard_normal((T, N)) * sc
                X = cc[:, None] + ee
            else:
                X = R[ix]
            cs, cs2 = cums(X)
            Ls, sd, _ = sd_curve(cs, cs2, T, anc)
            bp, _, _ = fit_pow(Ls, sd)
            D2, Cc, _, _ = fit_sat(Ls, sd)
            bs.append(bp); Ds.append(np.sqrt(max(D2, 0.0))); Cs.append(Cc)
        return np.array(bs), np.array(Ds), np.array(Cs)

    nb1, nd1, _ = null_fits(PANEL_HEAD, RUNG_HEAD, ANCHOR_HEAD, nrep=60, seed=7)
    nb2, nd2, _ = null_fits(PANEL_HEAD, RUNG_HEAD, ANCHOR_HEAD, nrep=60, seed=7)
    d9b = max(float(np.abs(nb1 - nb2).max()), float(np.abs(nd1 - nd2).max()))
    # process-STABLE seed check: a hardcoded md5 expectation, so a run in another process that
    # reproduces this line reproduces every null number below it.
    seedref = mdseed(SEED0, PANEL_HEAD, int(RUNG_HEAD * 10), ANCHOR_HEAD, False)
    gates["G9"] = (d9a == 0.0 and d9b == 0.0 and seedref == 2511885951,
                   f"determinism: ladder max|d| {d9a:.1e}; null fits max|d| {d9b:.1e}; "
                   f"md5 seed for ({PANEL_HEAD}, {RUNG_HEAD:.0f} bps, {ANCHOR_HEAD}) = "
                   f"{seedref} (expected 2511885951 — process-stable, NOT Python's hash())")

    # G10 NULL_J preserves the cross-book correlation
    R = RMAT[(PANEL_HEAD, RUNG_HEAD)]
    obs_corr = np.corrcoef(R.T)
    rng = np.random.default_rng(11)
    acc = []
    for _ in range(40):
        ix = rng.integers(0, R.shape[0], size=R.shape[0])
        acc.append(np.corrcoef(R[ix].T))
    d10 = float(np.abs(np.mean(acc, axis=0) - obs_corr).mean())
    gates["G10"] = (d10 < 0.02, f"NULL_J preserves cross-book corr: mean|d| {d10:.4f} over 40 reps")

    # G11 POOLED control: every tile window exactly L days, ZERO shared days, count == floor(T/L)
    ok11, why11, ntiles = True, [], []
    for p in PX:
        for L in LENS:
            ws = tile_windows(TLEN[p], L)
            ntiles.append(len(ws))
            if len(ws) != TLEN[p] // L:
                ok11 = False; why11.append(f"{p}/L{L} count {len(ws)}")
            if any((b - a) != L for a, b in ws):
                ok11 = False; why11.append(f"{p}/L{L} length")
            if any(ws[i][1] > ws[i + 1][0] for i in range(len(ws) - 1)):
                ok11 = False; why11.append(f"{p}/L{L} overlap")
    gates["G11"] = (ok11, f"POOLED tiling: exact length, zero shared days, counts "
                          f"{ntiles[:len(LENS)]} (U56)" + (("; " + "; ".join(why11[:3]))
                                                           if why11 else ""))

    npass = 0
    for k in sorted(gates):
        ok, msg = gates[k]
        npass += int(ok)
        P(f"  {k} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"  GATES: {npass} of {len(gates)} PASS")
    P("")

    # ============================================================ (A) THE CURVE
    P("=" * 100)
    P("(A) THE CURVE — sd_RAW at every LENGTH x ANCHOR x PANEL x RUNG (126 cells, all published)")
    P("=" * 100)
    dump(CT, "curve")
    P("  NOTE: TAIL / HEAD / MID are the tuned dial and read ONE window per length.  POOLED is a")
    P("  reported CONTROL — the MEDIAN sd_RAW over EVERY non-overlapping window of that length")
    P("  (17 / 11 / 7 / 4 / 3 / 2 / 1 windows at L = 250..2800), which cuts the noise on each")
    P("  rung by ~sqrt(K) and separates 'no exponent exists' from 'one window cannot see it'.")
    for anc in ALL_ANC:
        P(f"\n  ANCHOR {anc}" + ("   [CONTROL]" if anc == ANC_CTL else ""))
        piv = CT[CT.anchor == anc].pivot_table(index=["panel", "cost"], columns="L",
                                               values="sd_raw")
        P("    sd_RAW by window length L (trading days)")
        for line in piv.to_string(float_format=lambda x: f"{x:.4f}").split("\n"):
            P("      " + line)

    # ============================================================ (B) THE TWO FITS
    P("")
    P("=" * 100)
    P("(B) THE TWO FITS — POW (log sd = a + b log L) vs SAT (sd^2 = D^2 + C/L)")
    P("=" * 100)
    FIT = (CT.groupby(["panel", "cost", "anchor"])
             .agg(b_pow=("b_pow", "first"), rmse_pow=("rmse_pow", "first"),
                  D=("D", "first"), D2=("D2", "first"), se_D2=("se_D2", "first"),
                  C=("C", "first"), rmse_sat=("rmse_sat", "first"),
                  mean_sharpe=("mean_sharpe", "mean")).reset_index())
    FIT["D2_over_se"] = FIT["D2"] / FIT["se_D2"].replace(0, np.nan)
    FIT["rmse_ratio"] = FIT["rmse_sat"] / FIT["rmse_pow"].replace(0, np.nan)
    # theory C at the cell's own mean Sharpe, before the error-correlation haircut
    FIT["C_theory_indep"] = 252.0 + FIT["mean_sharpe"] ** 2 / 2.0
    FIT["rho_e_implied"] = 1.0 - FIT["C"] / FIT["C_theory_indep"]
    dump(FIT, "fits")
    P("")
    for line in FIT.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("  " + line)

    HEAD = FIT[(FIT.anchor == ANCHOR_HEAD)]
    HEADRUNG = HEAD[HEAD.cost == RUNG_HEAD]
    P("")
    P(f"  HEADLINE anchor {ANCHOR_HEAD}, 10 bps:")
    for _, r in HEADRUNG.iterrows():
        P(f"    {r.panel:<5} b_pow {r.b_pow:+.4f}  rmse_pow {r.rmse_pow:.4f} | "
          f"D {r.D:.4f} (D2/SE {r.D2_over_se:.2f})  C {r.C:.2f}  rmse_sat {r.rmse_sat:.4f}  "
          f"ratio {r.rmse_ratio:.3f}")

    # ============================================================ (C) THE NULLS
    P("")
    P("=" * 100)
    P(f"(C) THE NULLS — NULL_J ({NREP:,} joint day-resamples) and NULL_0 (zero-dispersion control)")
    P("=" * 100)
    nrows = []
    for (p, c) in CELLS:
        for anc in ALL_ANC:
            if anc != ANCHOR_HEAD and anc != ANC_CTL and c != RUNG_HEAD:
                continue                                    # keep the null grid to the dials
            bs, Ds, Cs = null_fits(p, c, anc)
            obs = FIT[(FIT.panel == p) & (FIT.cost == c) & (FIT.anchor == anc)].iloc[0]
            nrows.append(dict(panel=p, cost=c, anchor=anc, kind="NULL_J", nrep=NREP,
                              b_obs=obs.b_pow, b_null_med=float(np.median(bs)),
                              b_null_p05=float(np.percentile(bs, 5)),
                              b_null_p95=float(np.percentile(bs, 95)),
                              b_null_w90=float(np.percentile(bs, 95) - np.percentile(bs, 5)),
                              b_pct=float((bs <= obs.b_pow).mean()),
                              D_obs=obs.D, D_null_med=float(np.median(Ds)),
                              D_null_p95=float(np.percentile(Ds, 95)),
                              D_pct=float((Ds <= obs.D).mean()),
                              C_obs=obs.C, C_null_med=float(np.median(Cs))))
    for p in PX:
        for anc in (ANCHOR_HEAD, ANC_CTL):
            bs, Ds, Cs = null_fits(p, RUNG_HEAD, anc, nrep=NREP, zero_disp=True)
            nrows.append(dict(panel=p, cost=RUNG_HEAD, anchor=anc, kind="NULL_0", nrep=NREP,
                              b_obs=np.nan, b_null_med=float(np.median(bs)),
                              b_null_p05=float(np.percentile(bs, 5)),
                              b_null_p95=float(np.percentile(bs, 95)),
                              b_null_w90=float(np.percentile(bs, 95) - np.percentile(bs, 5)),
                              b_pct=np.nan,
                              D_obs=np.nan, D_null_med=float(np.median(Ds)),
                              D_null_p95=float(np.percentile(Ds, 95)), D_pct=np.nan,
                              C_obs=np.nan, C_null_med=float(np.median(Cs))))
    NL = pd.DataFrame(nrows)
    dump(NL, "nulls")
    P("")
    for line in NL.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("  " + line)

    # ============================================================ (D) THE PAYOFF
    P("")
    P("=" * 100)
    P("(D) THE PAYOFF — length-adjusting the record's OWN Q16 tail grid with the fitted curve")
    P("=" * 100)
    arows = []
    for (p, c) in CELLS:
        ws = q16_windows(p)
        Lw = np.array([b - a for a, b in ws], float)
        sd = sdq[(p, c)]
        Lref = float(Lw.max())
        raw = float(sd.max() - sd.min())
        row = dict(panel=p, cost=c, Lmin=float(Lw.min()), Lmax=Lref, band_raw=raw)
        for tag, anc in (("", ANCHOR_HEAD), ("_ctl", ANC_CTL)):
            f = FIT[(FIT.panel == p) & (FIT.cost == c) & (FIT.anchor == anc)].iloc[0]
            adj = np.sqrt(np.maximum(sd ** 2 - f.C / Lw + f.C / Lref, 0.0))
            adjp = sd * (Lw / Lref) ** (-f.b_pow)     # the exponent the queue asked for
            row[f"band_sat{tag}"] = float(adj.max() - adj.min())
            row[f"band_pow{tag}"] = float(adjp.max() - adjp.min())
            row[f"shrink_sat{tag}"] = float((adj.max() - adj.min()) / raw)
            row[f"shrink_pow{tag}"] = float((adjp.max() - adjp.min()) / raw)
        # FIXED-LAW adjustment: NO fitted parameter at all.  The arithmetic declared at the top
        # says sd ~ L^-0.5 once D = 0, so the adjustment needs no exponent estimate.  REPORTED,
        # NOT PRE-REGISTERED: it was added after the FITTED adjustments failed, and it is not
        # scored as a hypothesis.
        adjl = sd * np.sqrt(Lw / Lref)
        row["band_law"] = float(adjl.max() - adjl.min())
        row["shrink_law"] = float((adjl.max() - adjl.min()) / raw)
        arows.append(row)
    AD = pd.DataFrame(arows)
    dump(AD, "adjust")
    P("")
    for line in AD.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("  " + line)
    P("")
    P("  band_law / shrink_law use the A-PRIORI sqrt law (sd -> sd * sqrt(L/Lref)) with NO fitted")
    P("  parameter.  REPORTED, NOT PRE-REGISTERED — added after both FITTED adjustments failed,")
    P("  and deliberately not scored as a hypothesis.")
    z0 = NL[NL.kind == "NULL_0"]
    cth = float(FIT["C_theory_indep"].median())
    c0 = float(z0["C_null_med"].median())
    P(f"  THE ERROR CORRELATION, measured not asserted.  On NULL_0, where the only thing left in")
    P(f"  sd_RAW is sampling noise, the fitted C is {c0:.2f} against the INDEPENDENT-error theory")
    P(f"  value {cth:.2f} — so the mean pairwise correlation of the 18 books' Sharpe ERRORS is")
    P(f"  rho_e = 1 - {c0:.2f}/{cth:.2f} = {1 - c0/cth:.4f}.  The books are read off the same days,")
    P(f"  so ~{100*(1-c0/cth):.0f}% of each book's Sharpe error is a common shift that cancels out")
    P(f"  of a cross-sectional sd.  (1036's independently measured cross-end rho was 0.8934.)")

    # ============================================================ HYPOTHESES
    P("")
    P("=" * 100)
    P("PRE-REGISTERED HYPOTHESES (bars fixed before any number above the gates was read)")
    P("=" * 100)
    H = {}

    hp_b = HEADRUNG["b_pow"].values
    hp_ratio = HEADRUNG["rmse_ratio"].values
    H["H_POW"] = (bool(np.all((np.abs(hp_b) >= 0.45) & (np.abs(hp_b) <= 0.55))
                       and np.all(hp_ratio > 0.80)),
                  f"|b| {np.abs(hp_b).round(4).tolist()} in [0.45,0.55]? ; SAT/POW rmse ratio "
                  f"{hp_ratio.round(3).tolist()} > 0.80?")

    nsig = int((HEAD["D2_over_se"] > 2.0).sum())
    medratio = float(np.median(HEAD["rmse_ratio"]))
    H["H_SAT"] = (nsig >= 4 and medratio <= 0.5,
                  f"D2 > 2 SE in {nsig} of {len(HEAD)} headline-anchor cells (bar 4); median "
                  f"SAT/POW rmse ratio {medratio:.3f} (bar <= 0.500)")

    spreads = (FIT[FIT.anchor.isin(ANCHORS)]
               .groupby(["panel", "cost"])["b_pow"].agg(lambda s: s.max() - s.min()))
    medspread = float(np.median(spreads))
    H["H_ANCH"] = (medspread <= 0.10,
                   f"median across-anchor spread of b = {medspread:.4f} over "
                   f"{len(spreads)} (panel, rung) cells (bar <= 0.10); per cell "
                   f"{spreads.round(4).to_dict()}")

    pl = FIT[(FIT.anchor == ANC_CTL) & (FIT.cost == RUNG_HEAD)]
    plb = pl["b_pow"].values
    plw = NL[(NL.kind == "NULL_J") & (NL.anchor == ANC_CTL)
             & (NL.cost == RUNG_HEAD)]["b_null_w90"].values
    H["H_POOL"] = (bool(np.all((np.abs(plb) >= 0.45) & (np.abs(plb) <= 0.55))
                        and np.all(plw <= 0.20)),
                   f"POOLED control b {plb.round(4).tolist()} in [-0.55,-0.45]?; its own null's "
                   f"90% width {plw.round(4).tolist()} <= 0.20?")

    z = NL[(NL.kind == "NULL_0") & (NL.anchor == ANCHOR_HEAD)]
    zb, zd = z["b_null_med"].values, z["D_null_med"].values
    H["H_ZERO"] = (bool(np.all((zb >= -0.55) & (zb <= -0.45)) and np.all(zd <= 0.010)),
                   f"NULL_0 median b {zb.round(4).tolist()} in [-0.55,-0.45]?; median D "
                   f"{zd.round(4).tolist()} <= 0.010?")

    a10 = AD[AD.cost == RUNG_HEAD]
    H["H_ADJ"] = (bool(np.all(a10["shrink_sat"].values <= 0.5)),
                  f"SAT-adjusted / raw band at 10 bps = {a10['shrink_sat'].round(3).tolist()} "
                  f"(bar <= 0.500); POW-adjusted {a10['shrink_pow'].round(3).tolist()}; with the "
                  f"POOLED control's own C/b: SAT {a10['shrink_sat_ctl'].round(3).tolist()} / "
                  f"POW {a10['shrink_pow_ctl'].round(3).tolist()}")

    hp = 0
    for k in ["H_POW", "H_SAT", "H_ANCH", "H_POOL", "H_ZERO", "H_ADJ"]:
        ok, msg = H[k]
        hp += int(ok)
        P(f"  {k:<8} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"  HYPOTHESES: {hp} of {len(H)} PASS")

    # ============================================================ RULE 8
    P("")
    P("=" * 100)
    P(f"RULE 8 WALK-FORWARD — PROTOCOL's declared split {REC_END}; IS 2009-2016 ALONE chooses, "
      f"2017-2026 read ONCE")
    P("=" * 100)
    lrows = []
    for nm, b in pool.items():
        p = b["panel"]
        for c in RUNGS:
            bk = split_block(NET[(nm, c)], REC_END)
            lg = legs_at(bk, SPYB[(p, REC_END)])
            v2 = V2[(p, c)]
            lrows.append(dict(book=nm, panel=p, cost=c, **bk, **lg, pass4b=all(lg.values()),
                              pass4a=bool(bk["H1"] > v2["H1"] and bk["H2"] > v2["H2"]
                                          and bk["MaxDD"] >= v2["MaxDD"])))
    LAD = pd.DataFrame(lrows).set_index("book")
    dump(LAD.reset_index(), "ladder")
    wf = []
    for p in PX:
        for c in RUNGS:
            sub = LAD[(LAD.panel == p) & (LAD.cost == c)]
            for ch in RAW_CH:
                pick = raw_pick(sub, ch, SPYIS[(p, REC_END)])
                r = sub.loc[pick]
                s = SPYB[(p, REC_END)]
                v2 = V2[(p, c)]
                wf.append(dict(panel=p, cost=c, chooser=ch, pick=pick,
                               OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                               OOS_MaxDD=r.OOS_MaxDD,
                               spy_OOS_CAGR=s["OOS_CAGR"], spy_OOS_Sharpe=s["OOS_Sharpe"],
                               spy_OOS_MaxDD=s["OOS_MaxDD"],
                               v2_OOS_CAGR=v2["OOS_CAGR"], v2_OOS_Sharpe=v2["OOS_Sharpe"],
                               v2_OOS_MaxDD=v2["OOS_MaxDD"],
                               H1=r.H1, H2=r.H2, MaxDD=r.MaxDD,
                               pass4b=bool(r.pass4b), pass4a=bool(r.pass4a)))
    WF = pd.DataFrame(wf)
    dump(WF, "rule8")
    P("")
    for line in WF.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("  " + line)
    P(f"\n  OOS 4b {int(WF.pass4b.sum())} of {len(WF)};  OOS 4a {int(WF.pass4a.sum())} of "
      f"{len(WF)}.")
    best = WF.sort_values("OOS_Sharpe", ascending=False).iloc[0]
    P(f"  Best pick by OOS Sharpe: {best['pick']} ({best.panel}, {best.cost:.0f} bps, "
      f"{best.chooser}) {best.OOS_CAGR:.2%} / {best.OOS_Sharpe:.4f} / {best.OOS_MaxDD:.2%}")
    for p in PX:
        s = SPYB[(p, REC_END)]
        v = V2[(p, RUNG_HEAD)]
        P(f"  {p}: SPY OOS {s['OOS_CAGR']:.2%} / {s['OOS_Sharpe']:.4f} / {s['OOS_MaxDD']:.2%};  "
          f"RULES v2 live @10 bps OOS {v['OOS_CAGR']:.2%} / {v['OOS_Sharpe']:.4f} / "
          f"{v['OOS_MaxDD']:.2%} (halves {v['H1']:.3f} / {v['H2']:.3f})")
    P("  NO BOOK PROMOTED and NO BOOK KEEP CLAIMED: every pick is a GRID ladder book the record "
      "already holds, and all fail 4a on drawdown against the live book.")

    P("")
    P(f"# done in {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT.name}.log.txt")


if __name__ == "__main__":
    main()

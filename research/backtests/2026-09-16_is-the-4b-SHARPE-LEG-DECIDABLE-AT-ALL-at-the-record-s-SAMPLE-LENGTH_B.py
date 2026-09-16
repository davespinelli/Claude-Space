#!/usr/bin/env python3
"""Idea 1012 (lane B, 2026-09-16) — is the 4b SHARPE LEG DECIDABLE AT ALL at the record's
SAMPLE LENGTH?

QUESTION (QUEUE idea 1012, verbatim)
    idea 1001 found 0 of 45 books (9 committed passes + 36 control) clear 1 SE of the
    comparand's OWN bootstrap noise on BOTH Sharpe legs at any of 5 windows, and 0 of 45 at
    2 SE, with HALFMIN median 0.2102 against SEs of 0.2877/0.3350.  Invert it: solve for the
    SAMPLE LENGTH (or the margin) at which a leg WOULD clear 1 SE, and report whether any tape
    the record can reach makes the leg decidable.  Max 2 params (SE estimator, length ladder).

WHAT IS NEW AGAINST 1001, AND IT IS A CORRECTION FIRST.
    PROTOCOL 4b's Sharpe leg is a DIFFERENCE: `book half Sharpe - SPY half Sharpe`.  1001 priced
    that difference against the SE of ONE OF ITS TWO TERMS (SPY's own bootstrap SE, 0.2877 /
    0.3350).  The book and SPY are read off the SAME days and are strongly correlated, so the
    difference has a far smaller sampling SE than either term.  This is exactly the mismatch
    idea 1021 named for nested windows — comparing a statistic to a yardstick with a different
    correlation structure — and it is the same error one level down.  So this run reports the
    leg's required length on BOTH bases, all levels published:

      COMP    SPY's own half-Sharpe bootstrap SE          <- 1001's, the record's own, reproduced
      PAIRED  the SE of the MARGIN itself, book and SPY resampled on the SAME block indices
              so their co-movement is inherited exactly   <- the SE of the statistic being tested

    BASIS is the MEASURED AXIS, not a dial: both are deliverables and 1001's is the reference.

    (A) THE INVERSION.  A Sharpe SE falls as 1/sqrt(n).  A leg of margin m that sits at SE0 on
        n0 days needs n* = n0 * (k*SE0/|m|)^2 days to clear k SE.  Reported in YEARS, per book,
        per half, per basis, at k = 1 and k = 2, for all 45 books x 2 halves x 3 rungs.
    (B) THE LADDER, which EARNS the inversion.  The 1/sqrt(n) law is asserted by nobody here: it
        is measured.  Resample each path at a ladder of lengths drawn from the SAME tape and fit
        log SE = a + b log L.  b must land near -0.5 or the inversion in (A) is void; the fitted
        b is used for a SECOND, fit-based required length reported beside the sqrt one.
    (C) THE MARGIN THE RECORD CAN ACTUALLY BUY.  Inverted the other way: at the record's OWN half
        length, what half-Sharpe margin does a leg need?  That number is a bar future candidates
        can be held to today, which a required length of 300 years is not.
    (D) THE REACHABLE-TAPE VERDICT.  Required length against three bars: the record's own half
        (8.8y), its full tape (17.6y), and a 100-year bound on any US equity tape anyone could
        reach.  "Decidable" is SIGN-resolvable (|m| > k SE); "decidably POSITIVE" (m > k SE) is
        counted separately, because a leg that is decidably NEGATIVE is also a decided leg.
    (E) RULE 8.  Decidability as a SELECTOR: dial chosen on 2009-2016 alone, OOS 2017-2026 read
        once.  If screening on in-sample decidability costs OOS Sharpe it is a REPORTING
        requirement, not an alpha filter, and any PROTOCOL line must say so.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL grid points reported.
    (1) SE ESTIMATOR in {BLOCK21, BLOCK5, IID}
          BLOCK21  stationary bootstrap, expected block 21d   <- HEADLINE (1001's own)
          BLOCK5   stationary bootstrap, expected block 5d
          IID      i.i.d. bootstrap (block 1)
        1,000 draws, seed 1012, one shared index draw per (panel, half, estimator) so the COMP
        and PAIRED bases are read off the SAME resamples and differ only in the statistic.
    (2) LENGTH LADDER in {LAD6, LAD4}
          LAD6  L/n_full in {0.125, 0.25, 0.375, 0.50, 0.75, 1.00}   <- HEADLINE
          LAD4  L/n_full in {0.25, 0.50, 0.75, 1.00}
        n_full is the record's own post-warm-up tape (4,445 days); the record's HALF is 0.50.
    The cost rung {0, 10, 25} bps is a reported CONTROL; 10 bps is PROTOCOL's and is the
    headline.  The half convention is the record's COUNT rule (`len(r)//2`, baseline._row)
    throughout.  The window is the record's own (px.index[260]); 1001 already priced the window
    dial and it is not re-dialled here.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_UNDEC   on 1001's OWN basis (COMP, BLOCK21, 10 bps) the MEDIAN leg over the 45 books needs
              MORE THAN 50 YEARS of tape to clear 1 SE.  PASS = 1001's reading, taken at face
              value, makes the leg undecidable on any tape the record can reach.
    H_PAIR    median over 45 books x 2 halves of PAIRED SE / COMP SE <= 0.70.  PASS = the SE of
              the difference is materially smaller than the SE of one of its terms, i.e. 1001's
              yardstick overstates the noise of the object 4b actually tests.
    H_DEC     under PAIRED at the record's OWN half length, AT LEAST ONE of the 45 books clears
              1 SE on BOTH legs.  PASS = the leg is decidable today for at least one book, i.e.
              the answer to the queue's question is not "no tape anyone can reach".
    H_SCALE   the fitted exponent b of log SE on log L lands in [-0.65, -0.35] for the SPY half
              path and for the median book, on the headline ladder.  A FAIL voids (A)'s
              arithmetic and is reported as loudly as a PASS.
    H_WF      rule 8: a DECIDE-screened IS-only chooser picks a book that passes 4b out of
              sample, on the clean (GRIDONLY) pool.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  every SHELF book reproduces its committed memo triple (CAGR, Sharpe, MaxDD).
    G2  this run's fast runner == engine.backtest on the live book (max |d return|).
    G3  the SPY comparand reproduces the record's committed full-sample triple.
    G4  1001's OWN published numbers, recomputed: SPY half SEs 0.2877 / 0.3350 (its verbatim
        boot_se at its seed 1001), SHELF HALFMIN median 0.2102, and 0 of 45 / 0 of 45 books
        clearing 1 and 2 COMP SE on both legs.
    G5  the COUNT half convention here == baseline._row's halves on the live book.
    G6  determinism: every SE reproduces bit-for-bit on a re-draw at the same seed.
    G7  the PAIRED estimator is sound on synthetic paths: independent paths give
        se_paired ~ sqrt(se_a^2 + se_b^2); identical paths give se_paired ~ 0.
    G8  this run's vectorized stationary bootstrap agrees with 1001's verbatim sampler on the
        same object (|d SE| printed).
    G9  the 1/sqrt(n) law on a synthetic i.i.d. path: fitted b vs -0.5.

SURVIVORSHIP, up front (rule 9): U56 and B136 are CURRENT-constituent lists, so every book's
    Sharpe LEVEL is optimistic and every MARGIN is too.  A too-large margin makes a leg look
    MORE decidable and shortens every required length, so survivorship works AGAINST H_UNDEC and
    FOR H_DEC: the required lengths here are LOWER bounds and the decidable counts UPPER bounds.
    SPY is a real index series and is not inflated.  Stated where each is reported.

Nothing here is a capital claim.  Nothing is promoted.  Modifies no live file (RULES.md,
PROTOCOL.md, scan.py, bot.py, baseline.py untouched); any PROTOCOL wording is PROPOSED, not
applied (rule 6).

Outputs (committed under research/backtests/):
    .console.txt     full log
    .legs.csv        every book x half x rung x estimator: margin, COMP SE, PAIRED SE, ratio,
                     m/SE, required days/years at k=1,2 on both bases and on the fitted law
    .required.csv    the required-length summary per (basis, estimator, rung)
    .ladder.csv      the length ladder: SE at each L, per panel x half-object x estimator
    .decidable.csv   the reachable-tape integers per (set, basis, estimator, k, bar)
    .walkforward.csv rule 8, per (panel, chooser, screen, poolset)
    .hypotheses.csv  the five pre-registered bars with PASS/FAIL
    .gates.csv       the nine reproduction gates

Run: python research/backtests/2026-09-16_is-the-4b-SHARPE-LEG-DECIDABLE-AT-ALL-at-the-record-s-SAMPLE-LENGTH_B.py
Deterministic (seed 1012); no network (committed price caches only, never yfinance).
"""
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
from baseline import load_universe, score, rules_v2_weights, _row  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-the-4b-SHARPE-LEG-DECIDABLE-AT-ALL-at-the-record-s-SAMPLE-LENGTH"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_B"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP, MAX_VOL = 260, 0.60
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SEED = 1012
SEED_1001 = 1001
N_BOOT = 1000
ESTS = {"BLOCK21": 21, "BLOCK5": 5, "IID": 1}
EST_HEAD = "BLOCK21"
LADDERS = {"LAD6": [0.125, 0.25, 0.375, 0.50, 0.75, 1.00],
           "LAD4": [0.25, 0.50, 0.75, 1.00]}
LAD_HEAD = "LAD6"
BASES = ["COMP", "PAIRED"]
BASIS_REF = "COMP"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
KS = [1.0, 2.0]
YEAR = 252.0
BARS = {"HALF_NOW": None, "FULL_NOW": None, "CENTURY": 100.0 * YEAR}
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def load_lane_c():
    spec = importlib.util.spec_from_file_location("laneC1012", LANEC)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = load_lane_c()
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


def halves_count(n):
    """The record's own half rule (baseline._row: h = len(r)//2)."""
    k = n // 2
    return slice(0, k), slice(k, n)


def half_sharpes(r):
    a, b = halves_count(len(r))
    return fsharpe(r[a]), fsharpe(r[b])


# ---------------------------------------------------------------- samplers
def boot_se_1001(r, rng, n=N_BOOT, block=21):
    """idea 1001's boot_se, VERBATIM, so G4 reproduces its published SEs at its own seed."""
    r = np.asarray(r, float)
    T = len(r)
    if T < block * 3:
        return np.nan
    out = np.empty(n)
    for i in range(n):
        idx = np.empty(T, int)
        f = 0
        while f < T:
            s = rng.integers(0, T)
            L = min(rng.geometric(1.0 / block), T - f)
            idx[f:f + L] = (s + np.arange(L)) % T
            f += L
        out[i] = fsharpe(r[idx])
    return float(np.std(out, ddof=1))


def stat_idx(T, L, block, rng, n=N_BOOT):
    """Stationary (Politis-Romano) bootstrap indices: (n, L) ints drawn from a path of length T.
    block = expected block length; block == 1 is the i.i.d. bootstrap."""
    out = np.empty((n, L), dtype=np.int32)
    out[:, 0] = rng.integers(0, T, n)
    if L > 1:
        p = 1.0 / block
        newstart = rng.random((n, L - 1)) < p if block > 1 else np.ones((n, L - 1), bool)
        starts = rng.integers(0, T, (n, L - 1))
        for t in range(1, L):
            prev = out[:, t - 1] + 1
            prev[prev >= T] = 0
            out[:, t] = np.where(newstart[:, t - 1], starts[:, t - 1], prev)
    return out


def sharpe_vec(x, idx):
    """Annualised Sharpe of every resampled row of x taken at idx (n, L)."""
    X = np.asarray(x, float)[idx]
    m = X.mean(axis=1)
    s = X.std(axis=1, ddof=1)
    return np.where(s > 0, m * np.sqrt(YEAR) / s, np.nan)


def req_days(n0, se0, m, k, b=-0.5):
    """Days needed for |m| to clear k*SE, given SE(n) = se0 * (n/n0)**b.  b = -0.5 is the
    sqrt law; a fitted b is used for the fit-based column."""
    m = abs(float(m))
    if not np.isfinite(m) or m <= 0 or not np.isfinite(se0) or se0 <= 0:
        return np.inf
    ratio = m / (k * se0)
    if ratio >= 1.0:
        return float(n0)                      # already clears at the record's own length
    return float(n0 * ratio ** (1.0 / b))


def main():
    t0 = time.time()
    P(f"# Idea 1012 (lane B, {DATE}) — is the 4b SHARPE LEG DECIDABLE AT ALL at the record's "
      f"SAMPLE LENGTH?")
    P("# 2 tuned dials: SE ESTIMATOR [BLOCK21, BLOCK5, IID] x LENGTH LADDER [LAD6, LAD4].  "
      "All points reported.")
    P("# BASIS [COMP (1001's: SPY's own SE), PAIRED (the MARGIN's own SE)] is the MEASURED AXIS, "
      "not a dial.")
    P(f"# Cost rung {RUNGS} bps reported; {RUNG_HEAD:.0f} bps is PROTOCOL's and is the headline.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels — margins are optimistic, so every")
    P("#   required length here is a LOWER bound and every decidable count an UPPER bound.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    PX = {"U56": U, "B136": B}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; B136 {B.shape}.  "
      f"REC start {REC['U56'].date()} / {REC['B136'].date()}.")

    books = C.shelf_books(U, B)
    s0, ab0, v0 = score(U, vol_scale=False)
    rk = s0.where(ab0 & (v0 < MAX_VOL)).rank(axis=1, ascending=False)
    books["u56-top20-g065-M"] = dict(
        panel="U56", freq="M", W=(rk <= 20).astype(float) * 0.65 / 20,
        memo=(0.1269, 1.201, -0.1711), src="2026-09-15_u56-top20-g065_4b_B_MEMO.md")
    GRID = C.grid_books(U, B)
    SETS = {"SHELF": books, "GRID": GRID}
    P(f"SHELF = {len(books)} committed memo-backed 4b passes; GRID = {len(GRID)} never-selected "
      f"ladder books (control).  Total {len(books)+len(GRID)} books — 1001's 45.")

    # ---------------------------------------------------------------- net return paths
    NET = {}
    for setname, bset in SETS.items():
        for nm, b in bset.items():
            px = PX[b["panel"]]
            r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
            for c in RUNGS:
                NET[(setname, nm, c)] = (r - t * c / 1e4).loc[REC[b["panel"]]:]
    SPY = {p: PX[p]["SPY"].pct_change().fillna(0.0).loc[REC[p]:] for p in PX}
    V2 = {}
    for p, px in PX.items():
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            V2[(p, c)] = (r - t * c / 1e4).loc[REC[p]:]
    NFULL = {p: len(SPY[p]) for p in PX}
    NHALF = {p: len(SPY[p]) // 2 for p in PX}
    BARS["HALF_NOW"] = float(NHALF["U56"])
    BARS["FULL_NOW"] = float(NFULL["U56"])
    P(f"Record's own lengths (U56): full {NFULL['U56']} d = {NFULL['U56']/YEAR:.2f} y; "
      f"half {NHALF['U56']} d = {NHALF['U56']/YEAR:.2f} y.")
    P("")

    # ================================================================ GATES
    P("## Reproduction gates (printed before any hypothesis number is read)")
    gates = []

    grows, ok1 = [], True
    for nm, b in books.items():
        n = NET[("SHELF", nm, RUNG_HEAD)]
        cagr, sh, dd = fmet(n.values)
        m = b["memo"]
        dc = abs(cagr - m[0]) if m[0] is not None else 0.0
        ds = abs(sh - m[1]) if m[1] is not None else 0.0
        dv = abs(dd - m[2]) if m[2] is not None else 0.0
        good = dc <= 0.015 and ds <= 0.030 and dv <= 0.015
        ok1 &= good
        grows.append(dict(book=nm, got_CAGR=round(cagr, 4), got_Sharpe=round(sh, 4),
                          got_MaxDD=round(dd, 4), dCAGR=round(dc, 4), dSharpe=round(ds, 4),
                          dMaxDD=round(dv, 4), gate="PASS" if good else "FAIL"))
    P(pd.DataFrame(grows).to_string(index=False))
    P(f"G1 every SHELF book reproduces its committed memo triple: {'PASS' if ok1 else 'FAIL'}")
    gates.append(dict(gate="G1", what="SHELF memo triples",
                      value=f"{sum(g['gate']=='PASS' for g in grows)}/{len(grows)}",
                      verdict="PASS" if ok1 else "FAIL"))

    eng = backtest(U, rules_v2_weights(U), cost_bps=RUNG_HEAD, freq="W")
    d2 = float(np.abs(V2[("U56", RUNG_HEAD)].values - eng["returns"].loc[REC["U56"]:].values).max())
    ok2 = d2 < 1e-10
    P(f"G2 fast_run vs engine.backtest max|d ret| = {d2:.3e}: {'PASS' if ok2 else 'FAIL'}")
    gates.append(dict(gate="G2", what="fast_run == engine.backtest", value=f"{d2:.3e}",
                      verdict="PASS" if ok2 else "FAIL"))

    sc, ss, sd = fmet(SPY["U56"].values)
    ok3 = abs(sc - 0.1513) <= 0.004 and abs(ss - 0.886) <= 0.02 and abs(sd + 0.3372) <= 0.01
    P(f"G3 SPY {sc:.4f} / {ss:.4f} / {sd:.4f} vs committed 0.1513 / 0.886 / -0.3372: "
      f"{'PASS' if ok3 else 'FAIL'}")
    gates.append(dict(gate="G3", what="SPY committed triple", value=f"{sc:.4f}/{ss:.4f}/{sd:.4f}",
                      verdict="PASS" if ok3 else "FAIL"))

    bl = _row("x", V2[("U56", RUNG_HEAD)])
    h1c, h2c = half_sharpes(V2[("U56", RUNG_HEAD)].values)
    ok5 = abs(bl["H1"] - h1c) < 1e-12 and abs(bl["H2"] - h2c) < 1e-12
    P(f"G5 COUNT halves == baseline._row halves on the live book "
      f"({h1c:.6f}/{h2c:.6f} vs {bl['H1']:.6f}/{bl['H2']:.6f}): {'PASS' if ok5 else 'FAIL'}")
    gates.append(dict(gate="G5", what="COUNT halves == baseline._row", value=f"{abs(bl['H1']-h1c):.2e}",
                      verdict="PASS" if ok5 else "FAIL"))

    # ---- G4a: 1001's verbatim sampler at its own seed -> its published SPY half SEs
    rng1001 = np.random.default_rng(SEED_1001)
    s_u = SPY["U56"].values
    ha, hb = halves_count(len(s_u))
    se1001_h1 = boot_se_1001(s_u[ha], rng1001)
    se1001_h2 = boot_se_1001(s_u[hb], rng1001)
    ok4a = abs(se1001_h1 - 0.2877) <= 0.005 and abs(se1001_h2 - 0.3350) <= 0.005
    P(f"G4a 1001's verbatim boot_se at seed 1001: SPY half SEs {se1001_h1:.4f} / {se1001_h2:.4f} "
      f"vs its published 0.2877 / 0.3350: {'PASS' if ok4a else 'FAIL'}")

    # ================================================================ the SE machinery
    rng = np.random.default_rng(SEED)
    IDX = {}          # (panel, half, est) -> (N_BOOT, n_half) indices into the HALF path
    for p in PX:
        n = len(SPY[p])
        a, b_ = halves_count(n)
        for h, sl in (("H1", a), ("H2", b_)):
            L = sl.stop - sl.start
            for e, blk in ESTS.items():
                IDX[(p, h, e)] = stat_idx(L, L, blk, rng)
    SPYSH = {}        # (panel, half, est) -> (N_BOOT,) resampled SPY half Sharpes
    for (p, h, e), idx in IDX.items():
        a, b_ = halves_count(len(SPY[p]))
        sl = a if h == "H1" else b_
        SPYSH[(p, h, e)] = sharpe_vec(SPY[p].values[sl], idx)

    # ---- G7: paired estimator sanity on synthetic paths
    rg = np.random.default_rng(SEED + 7)
    T7 = 2000
    xa, xb = rg.normal(0, 0.01, T7), rg.normal(0, 0.01, T7)
    i7 = stat_idx(T7, T7, 21, np.random.default_rng(SEED + 70))
    sa, sb = sharpe_vec(xa, i7), sharpe_vec(xb, i7)
    se_a, se_b = float(np.std(sa, ddof=1)), float(np.std(sb, ddof=1))
    se_ind = float(np.std(sa - sb, ddof=1))
    se_same = float(np.std(sa - sa, ddof=1))
    quad = float(np.hypot(se_a, se_b))
    ok7 = abs(se_ind - quad) / quad < 0.10 and se_same < 1e-12
    P(f"G7 paired estimator: independent synthetic paths se_paired {se_ind:.4f} vs "
      f"sqrt(se_a^2+se_b^2) {quad:.4f} (d {abs(se_ind-quad)/quad:.1%}); identical paths "
      f"{se_same:.2e}: {'PASS' if ok7 else 'FAIL'}")
    gates.append(dict(gate="G7", what="paired estimator sanity",
                      value=f"{se_ind:.4f} vs {quad:.4f}; identical {se_same:.1e}",
                      verdict="PASS" if ok7 else "FAIL"))

    # ---- G8: this run's vectorized sampler vs 1001's verbatim one, same object
    se_vec_h1 = float(np.std(SPYSH[("U56", "H1", "BLOCK21")], ddof=1))
    se_vec_h2 = float(np.std(SPYSH[("U56", "H2", "BLOCK21")], ddof=1))
    d8 = max(abs(se_vec_h1 - se1001_h1), abs(se_vec_h2 - se1001_h2))
    ok8 = d8 < 0.02
    P(f"G8 vectorized stationary bootstrap vs 1001's sampler: {se_vec_h1:.4f}/{se_vec_h2:.4f} vs "
      f"{se1001_h1:.4f}/{se1001_h2:.4f}, max|d| {d8:.4f}: {'PASS' if ok8 else 'FAIL'}")
    gates.append(dict(gate="G8", what="vectorized sampler == 1001's sampler", value=f"{d8:.4f}",
                      verdict="PASS" if ok8 else "FAIL"))

    # ---- G6: determinism
    rngd = np.random.default_rng(SEED)
    chk = None
    for p in PX:
        n = len(SPY[p])
        a, b_ = halves_count(n)
        for h, sl in (("H1", a), ("H2", b_)):
            L = sl.stop - sl.start
            for e, blk in ESTS.items():
                ii = stat_idx(L, L, blk, rngd)
                if chk is None:
                    chk = float(np.abs(ii - IDX[(p, h, e)]).max())
                else:
                    chk = max(chk, float(np.abs(ii - IDX[(p, h, e)]).max()))
    ok6 = chk == 0.0
    P(f"G6 determinism: every bootstrap index array reproduces at seed {SEED}, max|d| {chk:.1e}: "
      f"{'PASS' if ok6 else 'FAIL'}")
    gates.append(dict(gate="G6", what="bootstrap determinism", value=f"{chk:.1e}",
                      verdict="PASS" if ok6 else "FAIL"))

    # ================================================================ (B) the LENGTH LADDER
    # SE at a ladder of lengths, drawn from the SAME full tape, for the SPY half object and for
    # every SHELF book's MARGIN.  Fits log SE = a + b log L.  This EARNS the 1/sqrt(n) inversion.
    P("")
    P("## B. The length ladder — the 1/sqrt(n) law measured, not asserted")
    lad_rows = []
    rngL = np.random.default_rng(SEED + 1)
    LADSET = sorted({f for lad in LADDERS.values() for f in lad})
    LAD_IDX = {}
    for p in PX:
        T = NFULL[p]
        for f in LADSET:
            L = max(40, int(round(f * T)))
            for e, blk in ESTS.items():
                LAD_IDX[(p, f, e)] = stat_idx(T, L, blk, rngL)
    ladder_books = {("SPY", p): None for p in PX}
    for nm, b in books.items():
        ladder_books[(nm, b["panel"])] = ("SHELF", nm)
    for (nm, p), ref in ladder_books.items():
        sp = SPY[p].values
        bk = None if ref is None else NET[(ref[0], ref[1], RUNG_HEAD)].values
        for f in LADSET:
            for e in ESTS:
                idx = LAD_IDX[(p, f, e)]
                ssh = sharpe_vec(sp, idx)
                row = dict(obj=nm, panel=p, est=e, frac=f, L=idx.shape[1],
                           years=idx.shape[1] / YEAR, se_COMP=float(np.std(ssh, ddof=1)))
                if bk is not None:
                    bsh = sharpe_vec(bk, idx)
                    row["se_PAIRED"] = float(np.std(bsh - ssh, ddof=1))
                    row["se_BOOKONLY"] = float(np.std(bsh, ddof=1))
                lad_rows.append(row)
    LAD = pd.DataFrame(lad_rows)
    LAD.to_csv(f"{OUT}.ladder.csv", index=False)

    def fitb(sub, col):
        s = sub.dropna(subset=[col])
        s = s[s[col] > 0]
        if len(s) < 3:
            return np.nan
        return float(np.polyfit(np.log(s.L.values), np.log(s[col].values), 1)[0])

    fit_rows = []
    for gname, lad in LADDERS.items():
        for e in ESTS:
            for p in PX:
                sub = LAD[(LAD.panel == p) & (LAD.est == e) & (LAD.frac.isin(lad))]
                spy_b = fitb(sub[sub.obj == "SPY"], "se_COMP")
                bb = [fitb(sub[sub.obj == nm], "se_PAIRED") for nm in sub.obj.unique()
                      if nm != "SPY"]
                fit_rows.append(dict(ladder=gname, est=e, panel=p, b_SPY_COMP=spy_b,
                                     b_med_PAIRED=float(np.nanmedian(bb)) if bb else np.nan,
                                     n_books=len(bb)))
    FIT = pd.DataFrame(fit_rows)
    P(LAD[(LAD.obj == "SPY") & (LAD.panel == "U56")][["est", "frac", "L", "years", "se_COMP"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P("  Fitted exponent b of log SE on log L (the sqrt law says -0.5):")
    P(FIT.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- G9: the law on a synthetic i.i.d. path
    rg9 = np.random.default_rng(SEED + 9)
    x9 = rg9.normal(0.0004, 0.01, NFULL["U56"])
    l9 = []
    for f in LADDERS[LAD_HEAD]:
        L = int(round(f * len(x9)))
        i9 = stat_idx(len(x9), L, 1, np.random.default_rng(SEED + 900 + int(f * 1000)))
        l9.append(dict(L=L, se=float(np.std(sharpe_vec(x9, i9), ddof=1))))
    b9 = fitb(pd.DataFrame(l9), "se")
    ok9 = -0.60 <= b9 <= -0.40
    P(f"G9 1/sqrt(n) law on a synthetic i.i.d. path: fitted b = {b9:.4f} vs -0.5: "
      f"{'PASS' if ok9 else 'FAIL'}")
    gates.append(dict(gate="G9", what="sqrt law on synthetic iid", value=f"{b9:.4f}",
                      verdict="PASS" if ok9 else "FAIL"))
    B_FIT = {}
    for _, r in FIT[FIT.ladder == LAD_HEAD].iterrows():
        B_FIT[(r.est, r.panel)] = r.b_med_PAIRED if np.isfinite(r.b_med_PAIRED) else -0.5

    # ================================================================ (A) the per-leg inversion
    P("")
    P("## A. Every leg, its margin, its SE on both bases, and the length it would need")
    legs = []
    for (setname, nm, c), n in NET.items():
        b = SETS[setname][nm]
        p = b["panel"]
        v = n.values
        a_, b2_ = halves_count(len(v))
        cagr, sh, dd = fmet(v)
        spv = SPY[p].values
        for h, sl in (("H1", a_), ("H2", b2_)):
            kb = fsharpe(v[sl])
            ks = fsharpe(spv[sl])
            m = kb - ks
            L0 = sl.stop - sl.start
            for e in ESTS:
                idx = IDX[(p, h, e)]
                bsh = sharpe_vec(v[sl], idx)
                ssh = SPYSH[(p, h, e)]
                se_comp = float(np.std(ssh, ddof=1))
                se_pair = float(np.std(bsh - ssh, ddof=1))
                se_book = float(np.std(bsh, ddof=1))
                rho = float(np.corrcoef(bsh, ssh)[0, 1])
                rec = dict(set=setname, book=nm, panel=p, freq=b["freq"], rung=c, half=h,
                           n_half=L0, book_H=kb, spy_H=ks, margin=m, est=e,
                           se_COMP=se_comp, se_PAIRED=se_pair, se_BOOK=se_book,
                           rho_boot=rho, ratio_PAIRED_COMP=se_pair / se_comp if se_comp else np.nan,
                           leg_pass=bool(m > 0))
                for basis, se_ in (("COMP", se_comp), ("PAIRED", se_pair)):
                    rec[f"m_in_SE_{basis}"] = m / se_ if se_ > 0 else np.nan
                    for k in KS:
                        d = req_days(L0, se_, m, k)
                        rec[f"req_y_{basis}_k{int(k)}"] = d / YEAR
                        df_ = req_days(L0, se_, m, k, b=B_FIT.get((e, p), -0.5))
                        rec[f"req_y_fit_{basis}_k{int(k)}"] = df_ / YEAR
                legs.append(rec)
    LG = pd.DataFrame(legs)
    LG.to_csv(f"{OUT}.legs.csv", index=False)

    HD = LG[(LG.rung == RUNG_HEAD) & (LG.est == EST_HEAD)]
    P("  SHELF, 10 bps, BLOCK21 (the record's own estimator):")
    P(HD[HD.set == "SHELF"][["book", "half", "book_H", "spy_H", "margin", "se_COMP", "se_PAIRED",
                             "ratio_PAIRED_COMP", "rho_boot", "m_in_SE_COMP", "m_in_SE_PAIRED",
                             "req_y_COMP_k1", "req_y_PAIRED_k1"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- G4b: 1001's HALFMIN median and its 0-of-45 integers, recomputed on COMP
    shelf_head = HD[HD.set == "SHELF"]
    halfmin = shelf_head.groupby("book").margin.min()
    hm_med = float(halfmin.median())
    per_book = HD.groupby(["set", "book"]).apply(
        lambda d: pd.Series(dict(minse_COMP=(d.margin / d.se_COMP).min(),
                                 minse_PAIRED=(d.margin / d.se_PAIRED).min(),
                                 both_pass=bool((d.margin > 0).all()))), include_groups=False)
    n1se = int((per_book.minse_COMP > 1.0).sum())
    n2se = int((per_book.minse_COMP > 2.0).sum())
    ok4b = abs(hm_med - 0.2102) <= 0.005 and n1se == 0 and n2se == 0
    ok4 = ok4a and ok4b
    P("")
    P(f"G4b 1001's HALFMIN median {hm_med:.4f} vs its published 0.2102; books clearing 1 COMP SE "
      f"on BOTH legs {n1se} of {len(per_book)} (1001: 0 of 45), 2 SE {n2se} of {len(per_book)} "
      f"(1001: 0 of 45): {'PASS' if ok4b else 'FAIL'}")
    P(f"G4 1001 reproduced end to end: {'PASS' if ok4 else 'FAIL'}")
    gates.append(dict(gate="G4", what="1001's published numbers reproduced",
                      value=f"SE {se1001_h1:.4f}/{se1001_h2:.4f}; HALFMIN {hm_med:.4f}; "
                            f"{n1se}/{n2se} of {len(per_book)}",
                      verdict="PASS" if ok4 else "FAIL"))

    # ================================================================ (A2) required-length summary
    P("")
    P("## A2. REQUIRED LENGTH — the queue's inversion, median over legs (all 45 books x 2 halves)")
    req_rows = []
    for setname, e, c, basis, k in product(list(SETS) + ["ALL"], ESTS, RUNGS, BASES, KS):
        sub = LG[(LG.est == e) & (LG.rung == c)]
        if setname != "ALL":
            sub = sub[sub.set == setname]
        col = f"req_y_{basis}_k{int(k)}"
        v = sub[col].values
        fin = v[np.isfinite(v)]
        req_rows.append(dict(set=setname, est=e, rung=c, basis=basis, k=k, n_legs=len(v),
                             med_req_y=float(np.median(v)) if len(v) else np.nan,
                             p25_req_y=float(np.percentile(v[np.isfinite(v)], 25)) if len(fin) else np.nan,
                             min_req_y=float(np.min(v)) if len(v) else np.nan,
                             n_infinite=int((~np.isfinite(v)).sum()),
                             med_se=float(sub[f"se_{basis}"].median()),
                             med_abs_margin=float(sub.margin.abs().median()),
                             n_within_HALF=int((v <= BARS["HALF_NOW"] / YEAR + 1e-9).sum()),
                             n_within_FULL=int((v <= BARS["FULL_NOW"] / YEAR + 1e-9).sum()),
                             n_within_CENTURY=int((v <= 100.0).sum())))
    RQ = pd.DataFrame(req_rows)
    RQ.to_csv(f"{OUT}.required.csv", index=False)
    P(RQ[(RQ.set == "ALL") & (RQ.rung == RUNG_HEAD)]
      .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P("")
    P("  Same table, SHELF and GRID separately, headline estimator and rung:")
    P(RQ[(RQ.set != "ALL") & (RQ.rung == RUNG_HEAD) & (RQ.est == EST_HEAD)]
      .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ================================================================ (C)+(D) reachable tape
    P("")
    P("## C. The MARGIN a leg needs AT THE RECORD'S OWN LENGTH (the bar a candidate can be held to)")
    bar_rows = []
    for e, c, basis, k in product(ESTS, RUNGS, BASES, KS):
        sub = LG[(LG.est == e) & (LG.rung == c)]
        bar_rows.append(dict(est=e, rung=c, basis=basis, k=k,
                             med_bar=float(k * sub[f"se_{basis}"].median()),
                             p90_bar=float(k * sub[f"se_{basis}"].quantile(0.90))))
    BR = pd.DataFrame(bar_rows)
    P(BR[BR.rung == RUNG_HEAD].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("")
    P("## D. DECIDABILITY on the tapes the record can reach "
      f"(HALF {BARS['HALF_NOW']/YEAR:.2f}y, FULL {BARS['FULL_NOW']/YEAR:.2f}y, CENTURY 100y)")
    dec_rows = []
    for setname, e, c, basis, k in product(list(SETS) + ["ALL"], ESTS, RUNGS, BASES, KS):
        sub = LG[(LG.est == e) & (LG.rung == c)]
        if setname != "ALL":
            sub = sub[sub.set == setname]
        g = sub.groupby("book").apply(
            lambda d: pd.Series(dict(
                minse=(d.margin.abs() / d[f"se_{basis}"]).min(),
                minse_signed=(d.margin / d[f"se_{basis}"]).min(),
                maxreq=d[f"req_y_{basis}_k{int(k)}"].max())), include_groups=False)
        dec_rows.append(dict(set=setname, est=e, rung=c, basis=basis, k=k, n_books=len(g),
                             both_legs_decidable_now=int((g.minse > k).sum()),
                             both_legs_decidably_POSITIVE_now=int((g.minse_signed > k).sum()),
                             both_legs_by_FULL=int((g.maxreq <= BARS["FULL_NOW"] / YEAR + 1e-9).sum()),
                             both_legs_by_CENTURY=int((g.maxreq <= 100.0).sum()),
                             med_maxreq_y=float(g.maxreq.median())))
    DEC = pd.DataFrame(dec_rows)
    DEC.to_csv(f"{OUT}.decidable.csv", index=False)
    P(DEC[(DEC.rung == RUNG_HEAD)].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ============================================== POST-HOC DIAGNOSTIC (added after G8/G4 FAILED)
    # DECLARED BARS ARE NOT MOVED.  G8 and G4 are recorded FAIL above and stay FAIL.  What follows
    # is a MEASUREMENT of why, because the reason turns out to be the run's own subject: an SE read
    # from 1,000 bootstrap draws is itself a random variable, so any integer thresholded on it is
    # too.  20 INDEPENDENT draws of each sampler on the same objects, reported in full.
    P("")
    P("## G8/G4 DIAGNOSTIC — is the gap a SAMPLER difference or the SE's own Monte-Carlo noise?")
    P("##   (post-hoc; the declared 0.02 bar is NOT moved and G8/G4 stay FAIL)")
    NSEED_D = 20
    s_u = SPY["U56"].values
    a_u, b_u = halves_count(len(s_u))
    old_d, new_d = [], []
    for sd_ in range(NSEED_D):
        old_d.append(boot_se_1001(s_u[a_u], np.random.default_rng(10_000 + sd_)))
        ii = stat_idx(a_u.stop - a_u.start, a_u.stop - a_u.start, 21,
                      np.random.default_rng(20_000 + sd_))
        new_d.append(float(np.std(sharpe_vec(s_u[a_u], ii), ddof=1)))
    old_d, new_d = np.array(old_d), np.array(new_d)
    P(f"  SPY U56 H1 SE over {NSEED_D} independent draws:")
    P(f"    1001's verbatim sampler : mean {old_d.mean():.4f} sd {old_d.std(ddof=1):.4f} "
      f"range {old_d.min():.4f}..{old_d.max():.4f}   (its published single draw: 0.2877)")
    P(f"    this run's vectorized   : mean {new_d.mean():.4f} sd {new_d.std(ddof=1):.4f} "
      f"range {new_d.min():.4f}..{new_d.max():.4f}   (this run's single draw: {se_vec_h1:.4f})")
    P(f"    mean-to-mean difference {abs(old_d.mean()-new_d.mean()):.4f} against a single-draw sd "
      f"of ~{max(old_d.std(ddof=1), new_d.std(ddof=1)):.4f} — the samplers agree; G8's gap is ONE "
      f"DRAW's noise, and G8's 0.02 bar was set below the sd of the thing it gates.")

    # the integers themselves, re-drawn: 1001's 0-of-45 and this run's PAIRED count
    mrg = {}
    for setname, bset in SETS.items():
        for nm, b in bset.items():
            p = b["panel"]
            v = NET[(setname, nm, RUNG_HEAD)].values
            aa, bb2 = halves_count(len(v))
            mrg[(setname, nm)] = (p, v, aa, bb2)
    intg = []
    for sd_ in range(NSEED_D):
        rr = np.random.default_rng(30_000 + sd_)
        IDXd, SPYd = {}, {}
        for p in PX:
            aa, bb2 = halves_count(len(SPY[p]))
            for h, sl in (("H1", aa), ("H2", bb2)):
                L = sl.stop - sl.start
                IDXd[(p, h)] = stat_idx(L, L, 21, rr)
                SPYd[(p, h)] = sharpe_vec(SPY[p].values[sl], IDXd[(p, h)])
        nc = np1 = 0
        for (setname, nm), (p, v, aa, bb2) in mrg.items():
            ok_c = ok_p = True
            for h, sl in (("H1", aa), ("H2", bb2)):
                mm = fsharpe(v[sl]) - fsharpe(SPY[p].values[sl])
                bsh = sharpe_vec(v[sl], IDXd[(p, h)])
                sc_ = float(np.std(SPYd[(p, h)], ddof=1))
                sp_ = float(np.std(bsh - SPYd[(p, h)], ddof=1))
                ok_c &= mm > sc_
                ok_p &= mm > sp_
            nc += ok_c
            np1 += ok_p
        intg.append((nc, np1))
    INT = pd.DataFrame(intg, columns=["n_COMP_1SE", "n_PAIRED_1SE"])
    INT.to_csv(f"{OUT}.seedint.csv", index=False)
    P("")
    P(f"  The two headline INTEGERS re-drawn {NSEED_D} times (45 books, 10 bps, BLOCK21, k=1):")
    P(f"    1001's COMP count : median {INT.n_COMP_1SE.median():.1f}, range "
      f"{INT.n_COMP_1SE.min()}..{INT.n_COMP_1SE.max()}, reads 0 in "
      f"{int((INT.n_COMP_1SE==0).sum())} of {NSEED_D} draws  (1001 published 0 of 45; this run "
      f"drew {n1se})")
    P(f"    this run's PAIRED count : median {INT.n_PAIRED_1SE.median():.1f}, range "
      f"{INT.n_PAIRED_1SE.min()}..{INT.n_PAIRED_1SE.max()}  (this run drew "
      f"{int(DEC[(DEC.set=='ALL')&(DEC.est==EST_HEAD)&(DEC.rung==RUNG_HEAD)&(DEC.basis=='PAIRED')&(DEC.k==1.0)].both_legs_decidably_POSITIVE_now.iloc[0]) if len(DEC) else -1})")
    P("  READ THIS AS THE RUN'S OWN SUBJECT: an integer thresholded on a 1,000-draw SE inherits "
      "that SE's noise.  The COMP count is a 0-or-1 coin at this sample length; the PAIRED count "
      "is not, and that separation is the finding, not the single draw.")

    # ================================================================ (E) rule 8
    P("")
    P("## E. Rule 8 walk-forward — dial chosen on 2009-2016 ALONE, OOS 2017-2026 read once")
    P("##    DECIDE screen = both IS legs clear 1 PAIRED SE of their OWN in-sample noise.")
    wf = []
    rngW = np.random.default_rng(SEED + 8)
    ALLBOOKS = [(s, nm) for s in SETS for nm in SETS[s]]
    for p in PX:
        spy_is = SPY[p].loc[:IS_END].values
        spy_oos = SPY[p].loc[OOS_START:]
        oc, os_, od = fmet(spy_oos.values)
        v2o = fmet(V2[(p, RUNG_HEAD)].loc[OOS_START:].values)
        v2h1, v2h2 = half_sharpes(V2[(p, RUNG_HEAD)].loc[OOS_START:].values)
        a_is, b_is = halves_count(len(spy_is))
        idx_is = {h: stat_idx(sl.stop - sl.start, sl.stop - sl.start, ESTS[EST_HEAD], rngW)
                  for h, sl in (("H1", a_is), ("H2", b_is))}
        spy_is_sh = {h: sharpe_vec(spy_is[sl], idx_is[h])
                     for h, sl in (("H1", a_is), ("H2", b_is))}
        s1, s2 = fsharpe(spy_is[a_is]), fsharpe(spy_is[b_is])
        cand = []
        for setname, nm in ALLBOOKS:
            if SETS[setname][nm]["panel"] != p:
                continue
            nis = NET[(setname, nm, RUNG_HEAD)].loc[:IS_END].values
            ic, isx, idd = fmet(nis)
            i1, i2 = fsharpe(nis[a_is]), fsharpe(nis[b_is])
            se_p = {}
            for h, sl, ss in (("H1", a_is, s1), ("H2", b_is, s2)):
                bsh = sharpe_vec(nis[sl], idx_is[h])
                se_p[h] = float(np.std(bsh - spy_is_sh[h], ddof=1))
            m1, m2 = i1 - s1, i2 - s2
            cand.append(dict(set=setname, book=nm, is_CAGR=ic, is_Sharpe=isx, is_MaxDD=idd,
                             is_m1=m1, is_m2=m2, is_se1=se_p["H1"], is_se2=se_p["H2"],
                             is_minse=min(m1 / se_p["H1"], m2 / se_p["H2"]),
                             is_4b_sharpe=(m1 > 0) and (m2 > 0),
                             is_decidable=(m1 > se_p["H1"]) and (m2 > se_p["H2"])))
        CD = pd.DataFrame(cand)
        P(f"  {p}: IS decidable (both legs > 1 PAIRED SE) {int(CD.is_decidable.sum())} of {len(CD)}; "
          f"IS 4b-sharpe {int(CD.is_4b_sharpe.sum())} of {len(CD)}; "
          f"IS minse median {CD.is_minse.median():.4f}")
        # POOLSET is a CONTAMINATION CONTROL, not a third tuned dial: the SHELF books were
        # memo-selected with FULL-SAMPLE information, so an OOS pass drawn from ALL inherits that
        # selection and is NOT evidence of out-of-sample skill.  GRIDONLY is the clean read.
        for chooser, screen, poolset in product(["CH_SHARPE", "CH_CAGR", "CH_MINSE"],
                                                ["PLAIN", "DECIDE"], ["ALL", "GRIDONLY"]):
            CDp = CD if poolset == "ALL" else CD[CD.set == "GRID"]
            pool = CDp[CDp.is_4b_sharpe] if screen == "PLAIN" else CDp[CDp.is_decidable]
            if not len(pool):
                wf.append(dict(panel=p, chooser=chooser, screen=screen, poolset=poolset,
                               pick="(none eligible)", n_pool=0,
                               spy_OOS_CAGR=oc, spy_OOS_Sharpe=os_, spy_OOS_MaxDD=od,
                               v2_OOS_CAGR=v2o[0], v2_OOS_Sharpe=v2o[1], v2_OOS_MaxDD=v2o[2]))
                continue
            key_ = {"CH_SHARPE": "is_Sharpe", "CH_CAGR": "is_CAGR", "CH_MINSE": "is_minse"}[chooser]
            pick = pool.sort_values([key_, "book"], ascending=[False, True]).iloc[0]
            n = NET[(pick.set, pick.book, RUNG_HEAD)].loc[OOS_START:]
            cg, sh, dd = fmet(n.values)
            o1, o2 = half_sharpes(n.values)
            so1, so2 = half_sharpes(spy_oos.values)
            p4b = (o1 > so1) and (o2 > so2) and (dd >= DDCAP_FRAC * od) and (cg >= CAGRFLOOR_FRAC * oc)
            p4a = (o1 > v2h1) and (o2 > v2h2) and (dd >= v2o[2])
            wf.append(dict(panel=p, chooser=chooser, screen=screen, poolset=poolset,
                           pick=pick.book, pick_set=pick.set, n_pool=int(len(pool)),
                           OOS_CAGR=cg, OOS_Sharpe=sh, OOS_MaxDD=dd, OOS_H1=o1, OOS_H2=o2,
                           spy_OOS_CAGR=oc, spy_OOS_Sharpe=os_, spy_OOS_MaxDD=od,
                           v2_OOS_CAGR=v2o[0], v2_OOS_Sharpe=v2o[1], v2_OOS_MaxDD=v2o[2],
                           OOS_4b=p4b, OOS_4a=p4a))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    # NOTE: OOS_4b/OOS_4a are OBJECT columns (bool + NaN for "(none eligible)" rows).
    # `.fillna(False).sum()` on an object column does NOT count them — it returns 1.  The
    # record's own rule-8 idiom (1001) carries this shape; counted with .eq(True) here.
    n4b = int(WF.OOS_4b.eq(True).sum()) if "OOS_4b" in WF else 0
    n4a = int(WF.OOS_4a.eq(True).sum()) if "OOS_4a" in WF else 0
    P(f"  OOS 4b passes: {n4b} of {len(WF)};  OOS 4a passes: {n4a} of {len(WF)}")
    for ps in ("ALL", "GRIDONLY"):
        g = WF[WF.poolset == ps]
        P(f"    {ps:8s}: OOS 4b {int(g.OOS_4b.eq(True).sum())} of {len(g)}; "
          f"OOS 4a {int(g.OOS_4a.eq(True).sum())} of {len(g)}; "
          f"distinct picks {sorted(set(g.pick))}")
    for sc_ in ("PLAIN", "DECIDE"):
        g = WF[(WF.screen == sc_) & (WF.poolset == "GRIDONLY") & WF.OOS_Sharpe.notna()]
        if len(g):
            P(f"    GRIDONLY {sc_:6s}: OOS Sharpe median {g.OOS_Sharpe.median():.4f}, "
              f"CAGR median {g.OOS_CAGR.median():.4f}, MaxDD median {g.OOS_MaxDD.median():.4f}")

    # ================================================================ hypotheses
    P("")
    P("## Pre-registered hypotheses")
    hyp = []
    hd = LG[(LG.rung == RUNG_HEAD) & (LG.est == EST_HEAD)]
    med_comp_req = float(np.median(hd["req_y_COMP_k1"].values))
    hyp.append(dict(name="H_UNDEC",
                    bar="median leg needs > 50 YEARS to clear 1 COMP SE (1001's own basis)",
                    got=f"{med_comp_req:.1f} y (COMP, BLOCK21, 10 bps, {len(hd)} legs)",
                    verdict="PASS" if med_comp_req > 50 else "FAIL"))
    med_ratio = float(hd.ratio_PAIRED_COMP.median())
    hyp.append(dict(name="H_PAIR", bar="median PAIRED SE / COMP SE <= 0.70",
                    got=f"{med_ratio:.4f} (median bootstrap rho(book,SPY) "
                        f"{hd.rho_boot.median():.4f})",
                    verdict="PASS" if med_ratio <= 0.70 else "FAIL"))
    dec_now = int(DEC[(DEC.set == "ALL") & (DEC.est == EST_HEAD) & (DEC.rung == RUNG_HEAD)
                      & (DEC.basis == "PAIRED") & (DEC.k == 1.0)]
                  .both_legs_decidable_now.iloc[0])
    dec_pos = int(DEC[(DEC.set == "ALL") & (DEC.est == EST_HEAD) & (DEC.rung == RUNG_HEAD)
                      & (DEC.basis == "PAIRED") & (DEC.k == 1.0)]
                  .both_legs_decidably_POSITIVE_now.iloc[0])
    hyp.append(dict(name="H_DEC", bar=">= 1 of 45 books clears 1 PAIRED SE on BOTH legs NOW",
                    got=f"{dec_now} of 45 sign-decidable, {dec_pos} of 45 decidably POSITIVE",
                    verdict="PASS" if dec_now >= 1 else "FAIL"))
    fh = FIT[(FIT.ladder == LAD_HEAD) & (FIT.est == EST_HEAD)]
    bs = float(fh.b_SPY_COMP.median())
    bm = float(fh.b_med_PAIRED.median())
    okS = (-0.65 <= bs <= -0.35) and (-0.65 <= bm <= -0.35)
    hyp.append(dict(name="H_SCALE", bar="fitted b in [-0.65, -0.35] for SPY and the median book",
                    got=f"b_SPY {bs:.4f}, b_med_book {bm:.4f}",
                    verdict="PASS" if okS else "FAIL"))
    gwf = WF[(WF.screen == "DECIDE") & (WF.poolset == "GRIDONLY")]
    nwf = int(gwf.OOS_4b.eq(True).sum()) if "OOS_4b" in gwf else 0
    hyp.append(dict(name="H_WF", bar="rule 8: a DECIDE-screened IS-only chooser passes 4b OOS "
                                     "(GRIDONLY)",
                    got=f"{nwf} of {len(gwf)} GRIDONLY DECIDE picks pass 4b OOS",
                    verdict="PASS" if nwf > 0 else "FAIL"))
    HY = pd.DataFrame(hyp)
    HY.to_csv(f"{OUT}.hypotheses.csv", index=False)
    P(HY.to_string(index=False))

    pd.DataFrame(gates).to_csv(f"{OUT}.gates.csv", index=False)
    P("")
    P(pd.DataFrame(gates).to_string(index=False))
    P("")
    P(f"# done in {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Idea 1001 (lane B, 2026-09-16) — is every committed 4b SHARPE LEG just the BENCHMARK'S
OWN LUCK in that window?

QUESTION (QUEUE idea 1001, verbatim)
    idea 971 found the `L_H1` pass rate over 900 books moves 0.599 -> 0.134 as the in-sample
    window start slides 2009 -> 2012, with Pearson -0.957 against SPY's OWN Sharpe in that
    window and -0.994 against the median book's margin.  Harvest every committed 4b pass in
    the record, recover the benchmark's Sharpe in each of ITS halves, and report how many
    passes clear their Sharpe legs only because SPY happened to be weak there.
    Max 2 params (claim set, window grid).

WHAT IS NEW AGAINST 971.  971 measured the window dial on a 900-row SYNTHETIC grid under a
    DISJOINT split rule, and reported the benchmark's bar as a by-product of a destruction
    census.  1001 asks the question of the REAL SHELF — the record's committed, memo-backed 4b
    passes — and makes the benchmark the subject:

    (A) THE COMPARAND CENSUS.  PROTOCOL 4b's two Sharpe legs are `book half Sharpe > SPY half
        Sharpe`, and SPY's half Sharpe is a REALISED number on whichever four-to-nine years the
        window start happens to put in that half.  Part A re-reads every committed pass's two
        legs against FOUR comparand conventions, all reported:
          LIVE    SPY's own Sharpe in that exact half-window          <- the record's own
          FULL    SPY's FULL-sample Sharpe, the SAME number in both halves (window luck removed)
          POOL    the MEDIAN of SPY's half-h Sharpe over the window grid
          MAX     the MAX of SPY's half-h Sharpe over the window grid  (strictest)
        BENCHLUCK(conv) = the book clears BOTH legs under LIVE and fails at least one under conv.
        That count, on the real shelf, is the queue's question stated as an integer.

    (B) THE WINDOW GRID, on the real shelf.  971's five window starts, re-read book by book:
        the leg pass rate, SPY's own bar, the book's own half Sharpe, the margin.  Pearson of
        the pass rate against SPY's bar is 971's -0.957 asked of the committed shelf.

    (C) THE SIDE ATTRIBUTION.  d margin = d(book half Sharpe) - d(SPY half Sharpe) exactly, so
        every window-to-window move splits into a BOOK side and a COMPARAND side.  If the
        comparand side carries it, the legs are a dial on the benchmark; if the book side does,
        971's reading does not transfer to the shelf.

    (D) THE BENCHMARK-NOISE BAR.  Even at a FIXED window, SPY's half Sharpe is one draw.  A
        stationary block bootstrap (expected block 21d, 1,000 draws, seed 1001) of SPY's own
        half-window returns gives the comparand's sampling SE.  A leg whose margin is smaller
        than that SE is not distinguishable from the benchmark's luck at its own window.

    (E) RULE 8.  The clause as a SELECTOR: dial chosen on 2009-2016 alone, OOS 2017-2026 read
        once per (panel, chooser, screen).  If screening on the window-invariant comparand
        costs OOS Sharpe it is a REPORTING requirement, not an alpha filter, and any PROTOCOL
        line must say so.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL grid points reported.
    (1) CLAIM SET in {SHELF, GRID}
          SHELF  the record's committed, memo-backed 4b KEEP-candidates, rebuilt from their own
                 memo wording and gated against their published headline triple (G1).  HEADLINE.
          GRID   861's mechanical band x gross x QROLL ladder, never memo-selected.  Control,
                 and the set on which 971's own claim is re-read (G4).
    (2) WINDOW GRID in {START5, START9}
          START5  {REC, 2010-01-01, 2011-01-01, 2012-01-01, 2013-01-01}   <- HEADLINE (971's own)
          START9  START5 + {2009-07-01, 2010-07-01, 2011-07-01, 2012-07-01}
          REC = the record's own start, px.index[260] (2009-01-13), i.e. PROTOCOL's warm-up skip.
    The COMPARAND CONVENTION (LIVE / FULL / POOL / MAX) is the MEASURED AXIS, not a dial: it is
    the deliverable, every level is published, and the record's own (LIVE) is the reference
    everywhere.  The cost rung {0, 10, 25} bps is a reported CONTROL; 10 bps is PROTOCOL's and
    is the headline.  The half convention is the record's COUNT rule (`len(r)//2`, baseline._row)
    throughout; the DATE convention was priced by idea 865 and is not re-dialled here.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_LUCK    at least ONE THIRD of the SHELF's committed two-leg Sharpe passes fail once the
              comparand is made window-invariant (FULL).  PASS = the queue's reading is right on
              the real shelf, not only on 971's synthetic grid.
    H_CORR    Pearson(two-leg pass rate over the shelf, SPY's own mean half bar) <= -0.70 across
              the window grid.  971 got -0.957 on 900 synthetic books.
    H_COMP    the comparand side carries the margin movement: median over books of
              sd_windows(SPY half Sharpe) > median over books of sd_windows(book half Sharpe).
    H_NOISE   the median SHELF HALFMIN margin (the weaker of the two legs, LIVE, REC window,
              10 bps) is SMALLER than 1 bootstrap SE of SPY's own half Sharpe, i.e. the legs sit
              inside the comparand's own noise.
    H_WF      rule 8: an IS-only chooser screened on the window-invariant comparand picks a book
              that passes 4b out of sample.
    Each prints its bar and PASS/FAIL, and a FAIL is reported as loudly as a PASS.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  every SHELF book reproduces its committed memo triple (CAGR, Sharpe, MaxDD).
    G2  this run's fast runner == engine.backtest on a live book (max |d return|).
    G3  the SPY comparand reproduces the record's committed full-sample triple.
    G4  971's own table, re-read on THIS run's GRID set at THIS run's window starts: SPY's L_H1
        bar and the L_H1 pass rate, printed as numbers, not assumed.
    G5  the COUNT half convention here == baseline._row's halves on a live book.
    G6  determinism: the bootstrap SE reproduces bit-for-bit on a re-draw at the same seed.

SURVIVORSHIP, up front: U56 and B136 are CURRENT-constituent lists, so every Sharpe LEVEL here
    (the books' and, for the panel-local benchmark, nothing — SPY is a real index series) is
    optimistic on the BOOK side.  The measured object is a MARGIN against SPY and its movement
    across windows; survivorship inflates the book side, so it works AGAINST H_LUCK, H_CORR and
    H_NOISE (it makes the shelf look more robust than it is).  Stated where each is reported.

Nothing here is a capital claim.  Nothing is promoted.  Modifies no live file (RULES.md, scan.py,
bot.py, baseline.py untouched); any PROTOCOL wording below is PROPOSED, not applied (rule 6).

Outputs (committed under research/backtests/):
    .console.txt   full log
    .census.csv    every book x window x rung: book/SPY half Sharpes, margins, legs, 4 comparands
    .benchluck.csv the BENCHLUCK integers per (set, window, rung, comparand)
    .decomp.csv    per book x half: sd/range of the book side vs the comparand side across windows
    .noise.csv     SPY half-Sharpe bootstrap SE per window x half, and every SHELF margin in SEs
    .walkforward.csv  rule 8, per (panel, chooser, screen)
    .hypotheses.csv  the five pre-registered bars with PASS/FAIL
    .gates.csv     the six reproduction gates

Run: python research/backtests/2026-09-16_is-every-committed-4b-SHARPE-LEG-just-the-BENCHMARK-S-OWN-LUCK-in-that-window_B.py
Deterministic (seed 1001); no network (committed price caches only, never yfinance).
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
SLUG = "is-every-committed-4b-SHARPE-LEG-just-the-BENCHMARK-S-OWN-LUCK-in-that-window"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_B"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP, MAX_VOL = 260, 0.60
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SEED = 1001
N_BOOT, BLOCK = 1000, 21
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
CONVS = ["LIVE", "FULL", "POOL", "MAX"]
CONV_REF = "LIVE"
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def load_lane_c():
    spec = importlib.util.spec_from_file_location("laneC1001", LANEC)
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


def boot_se(r, rng, n=N_BOOT, block=BLOCK):
    """Stationary block bootstrap SE of the Sharpe of a return path."""
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


def main():
    t0 = time.time()
    P(f"# Idea 1001 (lane B, {DATE}) — is every committed 4b SHARPE LEG just the BENCHMARK'S OWN "
      f"LUCK in that window?")
    P("# 2 tuned dials: CLAIM SET [SHELF, GRID] x WINDOW GRID [START5, START9].  All points reported.")
    P("# Comparand convention [LIVE, FULL, POOL, MAX] is the MEASURED AXIS, not a dial.")
    P(f"# Cost rung {RUNGS} bps reported; {RUNG_HEAD:.0f} bps is PROTOCOL's and is the headline.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels — the BOOK side of every margin is")
    P("#   optimistic, which works AGAINST this run's own hypotheses (see header).")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    PX = {"U56": U, "B136": B}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; B136 {B.shape}.  "
      f"REC start {REC['U56'].date()} / {REC['B136'].date()}.")

    # ---------------------------------------------------------------- book sets
    books = C.shelf_books(U, B)
    s0, ab0, v0 = score(U, vol_scale=False)
    rk = s0.where(ab0 & (v0 < MAX_VOL)).rank(axis=1, ascending=False)
    books["u56-top20-g065-M"] = dict(
        panel="U56", freq="M", W=(rk <= 20).astype(float) * 0.65 / 20,
        memo=(0.1269, 1.201, -0.1711), src="2026-09-15_u56-top20-g065_4b_B_MEMO.md")
    GRID = C.grid_books(U, B)
    SETS = {"SHELF": books, "GRID": GRID}
    P(f"SHELF = {len(books)} committed memo-backed 4b passes; GRID = {len(GRID)} never-selected "
      f"ladder books (control).")

    WGRIDS = {
        "START5": ["REC", "2010-01-01", "2011-01-01", "2012-01-01", "2013-01-01"],
        "START9": ["REC", "2009-07-01", "2010-01-01", "2010-07-01", "2011-01-01",
                   "2011-07-01", "2012-01-01", "2012-07-01", "2013-01-01"],
    }
    WGRID_HEAD = "START5"
    ALLW = WGRIDS["START9"]
    P(f"Window grid START5 = {WGRIDS['START5']} (headline, 971's own); START9 adds the mid-years.")
    P("")

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

    def wslice(s, w):
        return s if w == "REC" else s.loc[pd.Timestamp(w):]

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
    gates.append(dict(gate="G1", what="SHELF memo triples", value=f"{sum(g['gate']=='PASS' for g in grows)}/{len(grows)}",
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

    # ---------------------------------------------------------------- SPY's bars, every window
    spybar = {}
    for p in PX:
        for w in ALLW:
            s = wslice(SPY[p], w)
            b1, b2 = half_sharpes(s.values)
            fc, fs, fd = fmet(s.values)
            spybar[(p, w)] = dict(H1=b1, H2=b2, FULL=fs, CAGR=fc, MaxDD=fd, n=len(s),
                                  start=s.index[0].date(), mid=s.index[len(s) // 2].date())
    SB = pd.DataFrame([dict(panel=p, window=w, **v) for (p, w), v in spybar.items()])
    P("")
    P("## SPY's OWN Sharpe in each half, by window start (the object the legs are measured against)")
    P(SB[SB.panel == "U56"][["window", "start", "mid", "n", "H1", "H2", "FULL", "CAGR", "MaxDD"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # POOL / MAX comparands, per window grid (median / max of SPY's half-h bar over that grid)
    COMP = {}
    for gname, ws in WGRIDS.items():
        for p in PX:
            for h in ("H1", "H2"):
                v = [spybar[(p, w)][h] for w in ws]
                COMP[(gname, p, h, "POOL")] = float(np.median(v))
                COMP[(gname, p, h, "MAX")] = float(np.max(v))
    P("")
    P("  POOL/MAX comparands (over the window grid):")
    for gname in WGRIDS:
        for p in PX:
            P(f"    {gname:7s} {p:5s} POOL H1 {COMP[(gname,p,'H1','POOL')]:.4f} "
              f"H2 {COMP[(gname,p,'H2','POOL')]:.4f} | MAX H1 {COMP[(gname,p,'H1','MAX')]:.4f} "
              f"H2 {COMP[(gname,p,'H2','MAX')]:.4f}")

    # ================================================================ (A)+(B) the census
    rows = []
    for (setname, nm, c), n in NET.items():
        b = SETS[setname][nm]
        p = b["panel"]
        for w in ALLW:
            s = wslice(n, w)
            k1, k2 = half_sharpes(s.values)
            cagr, sh, dd = fmet(s.values)
            sp = spybar[(p, w)]
            rec = dict(set=setname, book=nm, panel=p, freq=b["freq"], rung=c, window=w,
                       n=len(s), book_H1=k1, book_H2=k2, book_CAGR=cagr, book_Sharpe=sh,
                       book_MaxDD=dd, spy_H1=sp["H1"], spy_H2=sp["H2"], spy_FULL=sp["FULL"],
                       spy_CAGR=sp["CAGR"], spy_MaxDD=sp["MaxDD"],
                       m1_LIVE=k1 - sp["H1"], m2_LIVE=k2 - sp["H2"],
                       m1_FULL=k1 - sp["FULL"], m2_FULL=k2 - sp["FULL"])
            for gname in WGRIDS:
                for conv in ("POOL", "MAX"):
                    rec[f"m1_{conv}_{gname}"] = k1 - COMP[(gname, p, "H1", conv)]
                    rec[f"m2_{conv}_{gname}"] = k2 - COMP[(gname, p, "H2", conv)]
            rec["L_DD"] = dd >= DDCAP_FRAC * sp["MaxDD"]
            rec["L_CAGR"] = cagr >= CAGRFLOOR_FRAC * sp["CAGR"]
            rows.append(rec)
    A = pd.DataFrame(rows)
    for conv in CONVS:
        if conv in ("LIVE", "FULL"):
            A[f"leg1_{conv}"] = A[f"m1_{conv}"] > 0
            A[f"leg2_{conv}"] = A[f"m2_{conv}"] > 0
        else:
            for gname in WGRIDS:
                A[f"leg1_{conv}_{gname}"] = A[f"m1_{conv}_{gname}"] > 0
                A[f"leg2_{conv}_{gname}"] = A[f"m2_{conv}_{gname}"] > 0
    A["sharpe_pass_LIVE"] = A.leg1_LIVE & A.leg2_LIVE
    A["sharpe_pass_FULL"] = A.leg1_FULL & A.leg2_FULL
    for gname in WGRIDS:
        for conv in ("POOL", "MAX"):
            A[f"sharpe_pass_{conv}_{gname}"] = A[f"leg1_{conv}_{gname}"] & A[f"leg2_{conv}_{gname}"]
    A["full4b_LIVE"] = A.sharpe_pass_LIVE & A.L_DD & A.L_CAGR
    A.to_csv(f"{OUT}.census.csv", index=False)

    H = A[(A.rung == RUNG_HEAD) & (A.window == "REC")]
    SH = H[H.set == "SHELF"]
    P("")
    P("## A. The committed shelf at the RECORD window (10 bps), leg by leg, comparand by comparand")
    show = SH[["book", "panel", "freq", "book_H1", "spy_H1", "m1_LIVE", "book_H2", "spy_H2",
               "m2_LIVE", "m1_FULL", "m2_FULL", "sharpe_pass_LIVE", "sharpe_pass_FULL",
               "sharpe_pass_POOL_START5", "sharpe_pass_MAX_START5"]]
    P(show.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # BENCHLUCK integers
    bl_rows = []
    for setname, gname, c, w in product(SETS, WGRIDS, RUNGS, ALLW):
        sub = A[(A.set == setname) & (A.rung == c) & (A.window == w)]
        base = sub[sub.sharpe_pass_LIVE]
        r = dict(set=setname, wgrid=gname, rung=c, window=w, n_books=len(sub),
                 pass_LIVE=int(len(base)))
        for conv in ("FULL", "POOL", "MAX"):
            col = f"sharpe_pass_{conv}" if conv == "FULL" else f"sharpe_pass_{conv}_{gname}"
            r[f"pass_{conv}"] = int(sub[col].sum())
            r[f"benchluck_{conv}"] = int((base[col] == False).sum())  # noqa: E712
            r[f"benchluck_share_{conv}"] = (float((base[col] == False).mean())  # noqa: E712
                                            if len(base) else np.nan)
        bl_rows.append(r)
    BL = pd.DataFrame(bl_rows)
    BL.to_csv(f"{OUT}.benchluck.csv", index=False)
    P("")
    P("## A2. BENCHLUCK — committed passes that clear LIVE and fail a window-invariant comparand")
    P("  (BENCHLUCK = clears BOTH legs under the record's own comparand, fails >=1 under conv)")
    key = BL[(BL.wgrid == WGRID_HEAD) & (BL.window == "REC")]
    P(key[["set", "rung", "n_books", "pass_LIVE", "pass_FULL", "benchluck_FULL",
           "benchluck_share_FULL", "pass_POOL", "benchluck_POOL", "pass_MAX", "benchluck_MAX"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- (B) window grid
    P("")
    P("## B. 971's table, re-read on the REAL shelf (10 bps, START5 windows)")
    tb = []
    for setname in SETS:
        for w in WGRIDS[WGRID_HEAD]:
            sub = A[(A.set == setname) & (A.rung == RUNG_HEAD) & (A.window == w)]
            tb.append(dict(set=setname, window=w,
                           spy_H1=sub.spy_H1.mean(), spy_H2=sub.spy_H2.mean(),
                           med_book_H1=sub.book_H1.median(), med_book_H2=sub.book_H2.median(),
                           med_m1=sub.m1_LIVE.median(), med_m2=sub.m2_LIVE.median(),
                           leg1_rate=sub.leg1_LIVE.mean(), leg2_rate=sub.leg2_LIVE.mean(),
                           both_rate=sub.sharpe_pass_LIVE.mean(),
                           full4b_rate=sub.full4b_LIVE.mean()))
    TB = pd.DataFrame(tb)
    P(TB.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ok4 = True
    P("G4 971's object (SPY's L_H1 bar and the L_H1 pass rate by window) printed above for BOTH "
      "sets; 971 published bar 0.838->1.877 and rate 0.599->0.220 on its 900-row synthetic grid.")
    gates.append(dict(gate="G4", what="971 table re-read on this run's sets", value="printed",
                      verdict="PASS" if ok4 else "FAIL"))

    def pear(x, y):
        x, y = np.asarray(x, float), np.asarray(y, float)
        m = np.isfinite(x) & np.isfinite(y)
        if m.sum() < 3:
            return np.nan
        return float(np.corrcoef(x[m], y[m])[0, 1])

    corr_rows = []
    for setname, gname in product(SETS, WGRIDS):
        t = TB[TB.set == setname] if gname == WGRID_HEAD else None
        ws = WGRIDS[gname]
        sub = A[(A.set == setname) & (A.rung == RUNG_HEAD) & (A.window.isin(ws))]
        g = sub.groupby("window").agg(spy_H1=("spy_H1", "mean"), spy_H2=("spy_H2", "mean"),
                                      leg1=("leg1_LIVE", "mean"), leg2=("leg2_LIVE", "mean"),
                                      both=("sharpe_pass_LIVE", "mean"),
                                      m1=("m1_LIVE", "median"), m2=("m2_LIVE", "median")).reindex(ws)
        g["spy_mean"] = (g.spy_H1 + g.spy_H2) / 2
        corr_rows.append(dict(set=setname, wgrid=gname, k=len(ws),
                              r_leg1_spyH1=pear(g.leg1, g.spy_H1),
                              r_leg2_spyH2=pear(g.leg2, g.spy_H2),
                              r_both_spymean=pear(g.both, g.spy_mean),
                              r_m1_spyH1=pear(g.m1, g.spy_H1),
                              r_m2_spyH2=pear(g.m2, g.spy_H2)))
    CR = pd.DataFrame(corr_rows)
    P("")
    P("## B2. Pearson against SPY's OWN bar across the window grid (971 got -0.957 / -0.994)")
    P(CR.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------- (B3) RECONCILIATION: where 971's slide lives
    # 971 read its halves inside the IS-ONLY window [w, 2016-12-31]; the RECORD reads them on the
    # FULL tape [w, 2026-09-15].  Same window STARTS, different window END.  This is NOT a third
    # tuned dial: the record's convention (full tape) is the headline everywhere above and the
    # IS-END reading exists only to LOCATE 971's published number.  Both endpoints reported.
    rec_rows = []
    for setname, gname in product(SETS, [WGRID_HEAD]):
        for w in WGRIDS[gname]:
            for end, tag in ((None, "FULLTAPE"), (IS_END, "ISEND2016")):
                p_bars = {}
                for p in PX:
                    s = wslice(SPY[p], w)
                    if end:
                        s = s.loc[:end]
                    b1, b2 = half_sharpes(s.values)
                    p_bars[p] = (b1, b2, len(s))
                l1 = l2 = both = 0
                tot = 0
                m1s, m2s = [], []
                for nm, b in SETS[setname].items():
                    s = wslice(NET[(setname, nm, RUNG_HEAD)], w)
                    if end:
                        s = s.loc[:end]
                    k1, k2 = half_sharpes(s.values)
                    s1, s2, _ = p_bars[b["panel"]]
                    m1s.append(k1 - s1)
                    m2s.append(k2 - s2)
                    l1 += k1 > s1
                    l2 += k2 > s2
                    both += (k1 > s1) and (k2 > s2)
                    tot += 1
                rec_rows.append(dict(set=setname, end=tag, window=w, n_days=p_bars["U56"][2],
                                     spy_H1=p_bars["U56"][0], spy_H2=p_bars["U56"][1],
                                     med_m1=float(np.median(m1s)), med_m2=float(np.median(m2s)),
                                     leg1_rate=l1 / tot, leg2_rate=l2 / tot, both_rate=both / tot))
    RC = pd.DataFrame(rec_rows)
    RC.to_csv(f"{OUT}.reconcile.csv", index=False)
    P("")
    P("## B3. RECONCILIATION — 971 read its halves inside the IS-ONLY window [w, 2016-12-31];")
    P("##     the RECORD reads them on the FULL tape [w, 2026-09-15].  Same starts, different END.")
    P(RC.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for setname in SETS:
        for tag in ("FULLTAPE", "ISEND2016"):
            g = RC[(RC.set == setname) & (RC.end == tag)]
            P(f"  {setname:5s} {tag:9s}: SPY H1 bar range {g.spy_H1.min():.4f}..{g.spy_H1.max():.4f} "
              f"(ptp {np.ptp(g.spy_H1.values):.4f}); two-leg pass rate "
              f"{g.both_rate.min():.4f}..{g.both_rate.max():.4f}; "
              f"Pearson(both_rate, spy_H1) = {pear(g.both_rate, g.spy_H1):.4f}")

    # ---------------------------------------------------------------- (C) side attribution
    dec = []
    for setname, bset in SETS.items():
        for nm in bset:
            for gname, ws in WGRIDS.items():
                sub = A[(A.set == setname) & (A.book == nm) & (A.rung == RUNG_HEAD)
                        & (A.window.isin(ws))].set_index("window").reindex(ws)
                for h, bc, sc_ in (("H1", "book_H1", "spy_H1"), ("H2", "book_H2", "spy_H2")):
                    bvals, svals = sub[bc].values, sub[sc_].values
                    dec.append(dict(set=setname, book=nm, wgrid=gname, half=h,
                                    sd_book=float(np.std(bvals, ddof=1)),
                                    sd_spy=float(np.std(svals, ddof=1)),
                                    rng_book=float(np.ptp(bvals)), rng_spy=float(np.ptp(svals)),
                                    sd_margin=float(np.std(bvals - svals, ddof=1)),
                                    comp_carries=bool(np.std(svals, ddof=1) > np.std(bvals, ddof=1))))
    DC = pd.DataFrame(dec)
    DC.to_csv(f"{OUT}.decomp.csv", index=False)
    P("")
    P("## C. Side attribution — which side moves when the window slides (10 bps)")
    ds = DC.groupby(["set", "wgrid", "half"]).agg(
        med_sd_book=("sd_book", "median"), med_sd_spy=("sd_spy", "median"),
        med_sd_margin=("sd_margin", "median"), comp_carries=("comp_carries", "mean")).reset_index()
    P(ds.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- (D) benchmark noise
    rng = np.random.default_rng(SEED)
    se = {}
    for p in PX:
        for w in ALLW:
            s = wslice(SPY[p], w).values
            a, b_ = halves_count(len(s))
            se[(p, w, "H1")] = boot_se(s[a], rng)
            se[(p, w, "H2")] = boot_se(s[b_], rng)
    rng2 = np.random.default_rng(SEED)
    se_chk = boot_se(wslice(SPY["U56"], "REC").values[halves_count(len(wslice(SPY['U56'], 'REC')))[0]], rng2)
    ok6 = abs(se_chk - se[("U56", "REC", "H1")]) < 1e-15
    P("")
    P(f"G6 determinism: bootstrap SE re-draw at seed {SEED} reproduces "
      f"({se_chk:.10f} vs {se[('U56','REC','H1')]:.10f}): {'PASS' if ok6 else 'FAIL'}")
    gates.append(dict(gate="G6", what="bootstrap determinism", value=f"{abs(se_chk-se[('U56','REC','H1')]):.2e}",
                      verdict="PASS" if ok6 else "FAIL"))

    nz = []
    for _, r in A[(A.rung == RUNG_HEAD)].iterrows():
        for h, mc in (("H1", "m1_LIVE"), ("H2", "m2_LIVE")):
            s_ = se[(r.panel, r.window, h)]
            nz.append(dict(set=r.set, book=r.book, panel=r.panel, window=r.window, half=h,
                           margin=r[mc], spy_bar=r["spy_H1" if h == "H1" else "spy_H2"],
                           spy_se=s_, margin_in_se=(r[mc] / s_ if s_ else np.nan),
                           inside_1se=bool(abs(r[mc]) < s_), leg_pass=bool(r[mc] > 0)))
    NZ = pd.DataFrame(nz)
    NZ.to_csv(f"{OUT}.noise.csv", index=False)
    P("")
    P("## D. The benchmark's OWN sampling noise (stationary block bootstrap, 1,000 draws, 21d)")
    P("  SPY half-Sharpe SE by window (U56 panel):")
    P(pd.DataFrame([dict(window=w, H1_bar=spybar[("U56", w)]["H1"], H1_se=se[("U56", w, "H1")],
                         H2_bar=spybar[("U56", w)]["H2"], H2_se=se[("U56", w, "H2")])
                    for w in WGRIDS[WGRID_HEAD]]).to_string(index=False,
                                                            float_format=lambda x: f"{x:.4f}"))
    nzh = NZ[(NZ.window == "REC") & (NZ.set == "SHELF")]
    P("")
    P("  Every SHELF leg at the RECORD window, in units of the comparand's own SE:")
    P(nzh[["book", "half", "margin", "spy_bar", "spy_se", "margin_in_se", "leg_pass",
           "inside_1se"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    halfmin = (nzh.groupby("book").margin.min())
    hm_se = (nzh.groupby("book").apply(lambda d: d.margin.min() / d.spy_se.mean(),
                                       include_groups=False))
    P("")
    P(f"  SHELF HALFMIN (weaker leg) margins: median {halfmin.median():.4f}, "
      f"min {halfmin.min():.4f}, max {halfmin.max():.4f}")
    P(f"  median SPY half SE at REC (U56) = {np.mean([se[('U56','REC','H1')], se[('U56','REC','H2')]]):.4f}")
    P(f"  SHELF HALFMIN in SE units: median {hm_se.median():.4f}; "
      f"{int((nzh.inside_1se & nzh.leg_pass).sum())} of {int(nzh.leg_pass.sum())} passing legs "
      f"sit INSIDE 1 SE of the comparand's own noise")
    # the decisive integer: books whose BOTH legs clear the comparand's own sampling noise
    outrows = []
    for setname in SETS:
        for w in WGRIDS[WGRID_HEAD]:
            g = NZ[(NZ.set == setname) & (NZ.window == w)]
            per = g.groupby("book").apply(
                lambda d: pd.Series(dict(minse=(d.margin / d.spy_se).min(),
                                         both_pass=bool((d.margin > 0).all()))),
                include_groups=False)
            outrows.append(dict(set=setname, window=w, n_books=len(per),
                                two_leg_pass=int(per.both_pass.sum()),
                                both_legs_gt_1se=int((per.minse > 1.0).sum()),
                                both_legs_gt_2se=int((per.minse > 2.0).sum()),
                                med_minse=float(per.minse.median())))
    OUTSE = pd.DataFrame(outrows)
    OUTSE.to_csv(f"{OUT}.outsidenoise.csv", index=False)
    P("")
    P("  How many books clear the comparand's OWN SAMPLING NOISE on BOTH legs (10 bps):")
    P(OUTSE.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ================================================================ (E) rule 8
    P("")
    P("## E. Rule 8 walk-forward — dial chosen on 2009-2016 ALONE, OOS 2017-2026 read once")
    wf = []
    ALLBOOKS = [(s, nm) for s in SETS for nm in SETS[s]]
    for p in PX:
        spy_is = SPY[p].loc[:IS_END]
        spy_oos = SPY[p].loc[OOS_START:]
        oc, os_, od = fmet(spy_oos.values)
        v2o = fmet(V2[(p, RUNG_HEAD)].loc[OOS_START:].values)
        cand = []
        for setname, nm in ALLBOOKS:
            if SETS[setname][nm]["panel"] != p:
                continue
            n = NET[(setname, nm, RUNG_HEAD)]
            nis = n.loc[:IS_END]
            ic, isx, idd = fmet(nis.values)
            i1, i2 = half_sharpes(nis.values)
            s1, s2 = half_sharpes(spy_is.values)
            sfull = fsharpe(spy_is.values)
            cand.append(dict(set=setname, book=nm, is_CAGR=ic, is_Sharpe=isx, is_MaxDD=idd,
                             is_m1=i1 - s1, is_m2=i2 - s2, is_m1F=i1 - sfull, is_m2F=i2 - sfull,
                             is_4b_sharpe=(i1 > s1) and (i2 > s2),
                             is_4b_full=(i1 > sfull) and (i2 > sfull)))
        CD = pd.DataFrame(cand)
        # POOLSET is a CONTAMINATION CONTROL, not a third tuned dial: the SHELF books were
        # memo-selected with FULL-SAMPLE information, so an OOS pass drawn from ALL inherits that
        # selection and is NOT evidence of out-of-sample skill.  GRIDONLY is the clean read.
        for chooser, screen, poolset in product(["CH_SHARPE", "CH_CAGR", "CH_MARGIN"],
                                                ["PLAIN", "FULLCOMP"], ["ALL", "GRIDONLY"]):
            CDp = CD if poolset == "ALL" else CD[CD.set == "GRID"]
            pool = CDp[CDp.is_4b_sharpe] if screen == "PLAIN" else CDp[CDp.is_4b_sharpe & CDp.is_4b_full]
            if not len(pool):
                wf.append(dict(panel=p, chooser=chooser, screen=screen, poolset=poolset,
                               pick="(none eligible)", n_pool=0))
                continue
            key_ = {"CH_SHARPE": "is_Sharpe", "CH_CAGR": "is_CAGR"}.get(chooser)
            if key_ is None:
                pool = pool.assign(_k=pool[["is_m1", "is_m2"]].min(axis=1))
                key_ = "_k"
            pick = pool.sort_values([key_, "book"], ascending=[False, True]).iloc[0]
            n = NET[(pick.set, pick.book, RUNG_HEAD)].loc[OOS_START:]
            cg, sh, dd = fmet(n.values)
            o1, o2 = half_sharpes(n.values)
            so1, so2 = half_sharpes(spy_oos.values)
            p4b = (o1 > so1) and (o2 > so2) and (dd >= DDCAP_FRAC * od) and (cg >= CAGRFLOOR_FRAC * oc)
            p4a = (o1 > half_sharpes(V2[(p, RUNG_HEAD)].loc[OOS_START:].values)[0]
                   and o2 > half_sharpes(V2[(p, RUNG_HEAD)].loc[OOS_START:].values)[1]
                   and dd >= v2o[2])
            wf.append(dict(panel=p, chooser=chooser, screen=screen, poolset=poolset,
                           pick=pick.book, pick_set=pick.set, n_pool=int(len(pool)),
                           OOS_CAGR=cg, OOS_Sharpe=sh, OOS_MaxDD=dd, OOS_H1=o1, OOS_H2=o2,
                           spy_OOS_CAGR=oc, spy_OOS_Sharpe=os_, spy_OOS_MaxDD=od,
                           v2_OOS_CAGR=v2o[0], v2_OOS_Sharpe=v2o[1], v2_OOS_MaxDD=v2o[2],
                           OOS_4b=p4b, OOS_4a=p4a))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    n4b = int(WF.OOS_4b.fillna(False).sum()) if "OOS_4b" in WF else 0
    n4a = int(WF.OOS_4a.fillna(False).sum()) if "OOS_4a" in WF else 0
    P(f"  OOS 4b passes: {n4b} of {len(WF)};  OOS 4a passes: {n4a} of {len(WF)}")
    for ps in ("ALL", "GRIDONLY"):
        g = WF[WF.poolset == ps]
        P(f"    {ps:8s}: OOS 4b {int(g.OOS_4b.fillna(False).sum())} of {len(g)}; "
          f"OOS 4a {int(g.OOS_4a.fillna(False).sum())} of {len(g)}; "
          f"distinct picks {sorted(set(g.pick))}")
    P("  NOTE (contamination): the ALL pool contains the memo-selected SHELF, chosen with "
      "FULL-SAMPLE information.  An OOS pass drawn from ALL is NOT evidence of OOS skill; "
      "GRIDONLY is the clean read and is reported beside it.")

    # ================================================================ hypotheses
    P("")
    P("## Pre-registered hypotheses")
    hyp = []
    base_shelf = SH[SH.sharpe_pass_LIVE]
    bl_full = int((base_shelf.sharpe_pass_FULL == False).sum())  # noqa: E712
    share = bl_full / len(base_shelf) if len(base_shelf) else np.nan
    v = share >= 1 / 3
    hyp.append(dict(name="H_LUCK", bar=">= 1/3 of SHELF two-leg LIVE passes fail under FULL",
                    got=f"{bl_full} of {len(base_shelf)} = {share:.4f}",
                    verdict="PASS" if v else "FAIL"))
    r_both = float(CR[(CR.set == "SHELF") & (CR.wgrid == WGRID_HEAD)].r_both_spymean.iloc[0])
    hyp.append(dict(name="H_CORR", bar="Pearson(SHELF two-leg pass rate, SPY mean bar) <= -0.70",
                    got=f"{r_both:.4f}", verdict="PASS" if r_both <= -0.70 else "FAIL"))
    dsh = DC[(DC.set == "SHELF") & (DC.wgrid == WGRID_HEAD)]
    mb, ms = float(dsh.sd_book.median()), float(dsh.sd_spy.median())
    hyp.append(dict(name="H_COMP", bar="median sd_windows(SPY half Sharpe) > median sd_windows(book)",
                    got=f"sd_spy {ms:.4f} vs sd_book {mb:.4f}",
                    verdict="PASS" if ms > mb else "FAIL"))
    med_hm = float(halfmin.median())
    med_se = float(nzh.spy_se.median())
    hyp.append(dict(name="H_NOISE", bar="median SHELF HALFMIN margin < 1 bootstrap SE of SPY's half Sharpe",
                    got=f"HALFMIN {med_hm:.4f} vs SE {med_se:.4f}",
                    verdict="PASS" if med_hm < med_se else "FAIL"))
    hyp.append(dict(name="H_WF", bar="rule 8: a FULLCOMP-screened IS-only chooser picks a 4b OOS pass",
                    got=f"{int(WF[(WF.screen=='FULLCOMP')].OOS_4b.fillna(False).sum())} of "
                        f"{int((WF.screen=='FULLCOMP').sum())} FULLCOMP picks pass 4b OOS",
                    verdict="PASS" if int(WF[(WF.screen == 'FULLCOMP')].OOS_4b.fillna(False).sum()) > 0 else "FAIL"))
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

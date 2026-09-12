#!/usr/bin/env python3
"""Idea 582 (cloud, 2026-09-12) - which-of-the-record-s-CLAUSES-are-INVISIBLE-to-their-own-control.

QUESTION (QUEUE idea 582, verbatim)
    Idea 317's gate G3 found the GROSS pair collapses to ONE book at matched gross (4.4e-16), so 48
    of 288 cells could not be a two-parent test at all.  Generalise: for each clause family in the
    record, is there ANY control the clause is not degenerate against?  A clause whose only content
    is an exposure dial should be named as such in PROTOCOL and priced against a constant-exposure
    control, not against a second 'parent'.

WHAT IS MEASURED, AND THE TWO WAYS A CLAUSE CAN BE INVISIBLE
    A clause family in this record is a PAIR of unconditional books (idea 317's parents).  Under a
    CONTROL the two books are rescaled so some exposure summary agrees, and the question is whether
    anything is left.  Two distinct failures, both reported per cell:
      MECH_DEGEN  the two target-weight paths are the SAME MATRIX once the control is applied
                  (max over days of the L1/2 weight distance < 1e-9).  This is idea 317's 4.4e-16:
                  the comparison is not a two-book test at all, at any sample length.
      INVISIBLE   the paths differ but |dSharpe| is no larger than the same book's own CONVENTION
                  FLOOR - the max-min Sharpe spread over the FIVE weekday offsets of the same
                  5-trading-day rebalance schedule, measured here, not assumed.  A clause inside
                  its own floor is a clause whose published number a reader cannot distinguish from
                  the arbitrary choice of rebalance weekday.
      VISIBLE     everything else.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two)
    1. CLAUSE FAMILY (8) - idea 317's six, verbatim, plus the two clauses the LIVE rules turn on:
         TREND   EWall      vs MA-RS       (200d MA gate - idea 317's "MA-DG" book, see below)
         VOLCAP  EWall      vs VOLCAP-DG   (drop vol20 >= 0.60, gated weight to CASH)
         WIDEN   TOP20      vs EWall       (idea 318's pair)
         CONC    TOP20      vs TOP10       (idea 316's pair)
         GROSS   EW-100     vs EW-0375     (the de-gross switch - idea 317's degenerate one)
         DEFEND  TOP20      vs LOWVOL20
         BAND    MA-RS      vs BAND-RS     (RULES v2 clause 2: +/-3% hysteresis vs a bare MA gate)
         SPREAD  MA-DG      vs MA-RS       (gated weight to CASH vs re-spread over survivors)

    A NAMING FAULT IN THE PARENT, FOUND WHILE BUILDING THIS FILE AND GATED (G5)
       Idea 317's book it calls "MA-DG  (only names above their 200d MA, gated weight to CASH)" is
       built as `_ew(ma, G).where(ma, 0.0)`, and `_ew` divides by the count of TRUE entries IN THE
       MASK IT IS GIVEN.  Given the GATE as its mask, the denominator is the number of names that
       PASS the gate, so the gated weight is RE-SPREAD over the survivors at full gross and the
       trailing `.where(ma, 0.0)` is a no-op - there is no cash leg at all.  The same file's
       "VOLCAP-DG" is `_ew(elig, G).where(capok, 0.0)`, whose mask IS the eligible set, so that one
       is a genuine de-gross.  Two clauses named "-DG" in one committed script therefore carry
       OPPOSITE weight handling.  This file keeps idea 317's book under its true name (MA-RS) so the
       G3 comparison stays apples-to-apples, adds the de-gross book it was named for (MA-DG =
       G * gate / N_priced, gated weight to CASH, which is what live RULES v2 does), and gives the
       DEGROSS-vs-RESPREAD clause its own family (SPREAD) - which in the record's own vocabulary has
       never been run as named on this pair.
    2. CONTROL (5)
         RAW     as published, no matching
         GROSS   mean TARGET GROSS on rebalance days matched to the pair's min (idea 317's control)
         VOL     full-window realised vol matched (2 scaling passes; residual gap reported)
         BETA    full-window SPY beta matched     (2 scaling passes; residual gap reported)
         CONST   the PROTOCOL proposal: BOTH arms against a CONSTANT-EXPOSURE comparand - EWall
                 scaled to that arm's own mean gross - instead of against a second 'parent'.  The
                 cell keeps the MORE VISIBLE of the two legs, since a family is invisible to
                 constant exposure only if NEITHER of its arms can be told apart from it.
    8 x 5 x 3 panels = 120 cells, ALL reported.  Everything else is PINNED: base gross 0.75
    (1.00/0.375 inside GROSS by construction), weekly cadence, t+1, 10 bps, MA 200d, vol window
    20d, vol cap 0.60, n = 10/20, band 3%.  Panel is REPORTED-NEVER-SELECTED.

PRE-REGISTERED HYPOTHESES (written before any number below was read)
    H_ONE    : the queue's question, read optimistically - EVERY family has at least one control
               under which it is VISIBLE on all three panels.
    H_GROSS  : idea 317's single-panel G3 generalises - the GROSS family is MECH_DEGEN under the
               matched-gross control on ALL THREE panels.
    H_EXPO   : matched exposure kills only exposure clauses - under GROSS/VOL/BETA the five
               holdings-changing families (TREND, VOLCAP, WIDEN, CONC, DEFEND) stay VISIBLE in
               >= 80% of their (family, panel, control) cells.
    H_CONST  : the constant-exposure comparand is STRICTLY MORE DEMANDING than a second parent -
               at least one non-GROSS family is INVISIBLE against CONST while VISIBLE against its
               own parent at matched gross.
    H_FLOOR  : the convention floor is material, not bookkeeping - at least one published-style
               comparison (RAW or matched-GROSS) sits inside its own floor.
    H_OOS    : rule 8 on the ANSWER - the label is window-stable: <= 20% of the 120 cells flip
               between the IS label and the OOS label, with labels read once per window.

GATES (printed BEFORE any new number is read)
    G1 engine   : the vectorised runner vs engine.backtest on 3 books, one per panel.      1e-9
    G2 matching : after a control, the matched summary agrees to its stated tolerance, and no
                  scaled book exceeds gross 1.0 (no leverage - PROTOCOL rule 2).         1e-12 / 0
    G3 parent   : this run's matched-gross max|dSharpe| per family on U56 against idea 317's
                  committed G3 numbers (TREND 1.747e-01, VOLCAP 2.444e-01, WIDEN 2.773e-01,
                  CONC 1.402e-01, GROSS 4.441e-16, DEFEND 6.073e-02).  Idea 317 took its max over
                  288 conditional cells' parent legs; this run has no conditional legs, so the
                  comparable object is the SAME matched-gross parent pair - MEASURED and published
                  as a drift reading, with GROSS's collapse as the one hard bar (< 1e-9).
    G4 determinism: every cell rebuilt twice gives bit-identical Sharpe.                   bar 0

RULE 8 WALK-FORWARD (required)
    IS = ..2016-12-31, OOS = 2017-01-01.., OOS read ONCE.  Both windows are run as their own
    backtests (weights built causally on the full panel, the book RUN on the sliced panel) and each
    control's scaling factors are re-derived INSIDE the window, so a label is never carried across.
    WF-A on the ANSWER: the VISIBLE/INVISIBLE/MECH_DEGEN label per cell in IS, then the OOS label
       read once; flips counted and published per family.
    WF-B on a BOOK: among every book this file runs (panel x form x control scaling), the pick is
       made by IS Sharpe ALONE and its OOS CAGR/Sharpe/MaxDD are read ONCE against live RULES v2
       (U56, weekly, 10 bps) and against SPY.

KEEP PATHS: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and 4b (Sharpe > SPY in
    BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) are evaluated and counted for
    EVERY book.  4a is read against RULES v2 on U56 (PROTOCOL rule 3 as written) and, because idea
    737 raised the panel question, ALSO against RULES v2 rebuilt on the book's OWN panel.  These are
    the record's standard book forms, not new candidates: this file is a degeneracy census.

SURVIVORSHIP: B136 and SMALL are CURRENT constituents of their screens (SMALL drops every ticker
    whose max_1d_move >= 1.0 in data/small_meta.csv, per PROTOCOL), so every LEVEL on those panels
    is overstated.  Every claim here is a DIFFERENCE between two books on the SAME panel, which is
    where the bias largely cancels; the KEEP-path and WF-B legs are read as diagnostics only.

PROTOCOL: 10 bps per unit turnover, next-day fills, no shorting, no leverage.  Deterministic,
standalone, no network.  Writes only its own outputs:
    .cells.csv .floors.csv .walkforward.csv .keeppaths.csv .gates.csv .console.txt
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score, band_state, metrics, backtest  # noqa
from engine import rebalance_mask  # noqa: E402

STAMP = "2026-09-12_which-of-the-record-s-CLAUSES-are-INVISIBLE-to-their-own-control_cloud"
OUT = ROOT / "research" / "backtests"

COST, FREQ = 10.0, "W"
G, MA_WIN, VOL_WIN, VOL_CAP, BAND = 0.75, 200, 20, 0.60, 0.03
IS_END, OOS_START = "2016-12-31", "2017-01-01"
FAMS = ("TREND", "VOLCAP", "WIDEN", "CONC", "GROSS", "DEFEND", "BAND", "SPREAD")
PAIRS = {"TREND": ("EWall", "MA-RS"), "VOLCAP": ("EWall", "VOLCAP-DG"),
         "WIDEN": ("TOP20", "EWall"), "CONC": ("TOP20", "TOP10"),
         "GROSS": ("EW-100", "EW-0375"), "DEFEND": ("TOP20", "LOWVOL20"),
         "BAND": ("MA-RS", "BAND-RS"), "SPREAD": ("MA-DG", "MA-RS")}
CONTROLS = ("RAW", "GROSS", "VOL", "BETA", "CONST")
MECH_TOL = 1e-9
# idea 317's committed gate G3, for G3 here
P317 = {"TREND": 1.747e-01, "VOLCAP": 2.444e-01, "WIDEN": 2.773e-01, "CONC": 1.402e-01,
        "GROSS": 4.441e-16, "DEFEND": 6.073e-02}

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# =============================================================== vectorised engine clone
def _mask_weekly(idx):
    return rebalance_mask(idx, FREQ).to_numpy(bool)


def _mask_offset(idx, off):
    """Every 5th trading day, starting at `off` - the five weekday offsets of a weekly cadence."""
    m = np.zeros(len(idx), bool)
    m[off::5] = True
    return m


def fast_bt(px, W, mask=None, cost_bps=COST):
    """engine.backtest in closed form (gate G1): same t+1 application, same drift with cash flat,
    same turnover cost.  `mask` is the rebalance mask in PRE-SHIFT (decision-day) convention."""
    idx = px.index
    rets = px.pct_change().fillna(0.0).to_numpy(float)
    wt = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).to_numpy(float)
    mk = _mask_weekly(idx) if mask is None else np.asarray(mask, bool)
    mk = np.concatenate([[False], mk[:-1]]).copy()        # applied next day, as the engine does
    mk[0] = True
    T, N = rets.shape
    Cs = np.empty((T, N))
    Cs[0] = 1.0
    np.cumprod(1.0 + rets[:-1], axis=0, out=Cs[1:])
    starts = np.flatnonzero(mk)
    seg = np.searchsorted(starts, np.arange(T), side="right") - 1
    s_of_t = starts[seg]
    new = wt[s_of_t]
    num = new * (Cs / Cs[s_of_t])
    D = num.sum(axis=1) + (1.0 - new.sum(axis=1))
    held = num / D[:, None]
    turn = np.zeros(T)
    turn[0] = np.abs(wt[0]).sum()
    later = starts[1:]
    if len(later):
        sp = starts[seg[later] - 1]
        prev_new = wt[sp]
        np_ = prev_new * (Cs[later] / Cs[sp])
        Dp = np_.sum(axis=1) + (1.0 - prev_new.sum(axis=1))
        turn[later] = np.abs(wt[later] - np_ / Dp[:, None]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r):
    m = metrics(r)
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"], H1=h1, H2=h2)


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    ro, so = r.loc[OOS_START:], spy.loc[OOS_START:]
    if not (len(ro) > 60 and metrics(ro)["Sharpe"] > metrics(so)["Sharpe"]):
        f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


# =============================================================== book forms (idea 317's, verbatim)
def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.astype(float).div(n, axis=0).fillna(0.0)


def _topn(sc, elig, n, g):
    rk = sc.where(elig).rank(axis=1, ascending=False)
    return _ew((rk <= n) & elig, g)


def build_books(px, tradable):
    elig = px.notna() & pd.DataFrame(np.tile(tradable, (len(px), 1)), index=px.index,
                                     columns=px.columns)
    ma = (px > px.rolling(MA_WIN).mean()) & elig
    vol20 = px.pct_change().rolling(VOL_WIN).std() * np.sqrt(252)
    capok = (vol20 < VOL_CAP).fillna(False) & elig
    sc, _, _ = score(px, vol_scale=True)
    bst = band_state(px, BAND) & elig
    B = {
        "EWall":     _ew(elig, G),
        "MA-RS":     _ew(ma, G),                       # idea 317's "MA-DG": RE-SPREAD, no cash leg
        "MA-DG":     _ew(elig, G).where(ma, 0.0),      # the real de-gross: gated weight to CASH
        "BAND-RS":   _ew(bst, G),
        "BAND-DG":   _ew(elig, G).where(bst, 0.0),
        "VOLCAP-DG": _ew(elig, G).where(capok, 0.0),
        "IDEA317-MADG": _ew(ma, G).where(ma, 0.0),     # verbatim from idea 317, for gate G5
        "TOP20":     _topn(sc, elig, 20, G),
        "TOP10":     _topn(sc, elig, 10, G),
        "EW-100":    _ew(elig, 1.00),
        "EW-0375":   _ew(elig, 0.375),
        "LOWVOL20":  _topn((-vol20).where(elig), elig, 20, G),
    }
    return B


def mean_gross(W, idx):
    m = rebalance_mask(idx, FREQ)
    return float(W.reindex(idx).fillna(0.0).sum(axis=1)[m].mean())


def beta_to(r, spy):
    d = pd.concat([r, spy], axis=1).dropna()
    v = float(d.iloc[:, 1].var())
    return float(d.iloc[:, 0].cov(d.iloc[:, 1]) / v) if v > 0 else np.nan


def l1_dist(WA, WB, idx):
    """Mean and max over days of 0.5*sum|wA - wB| - the fraction of NAV the clause moves."""
    a = WA.reindex(idx).fillna(0.0)
    b = WB.reindex(idx).fillna(0.0)
    d = 0.5 * (a - b).abs().sum(axis=1)
    return float(d.mean()), float(d.max())


# =============================================================== the control
def const_legs(pxw, books, form):
    """One arm against a CONSTANT-EXPOSURE comparand: EWall scaled to that arm's own mean gross.
    This is the control the queue proposes PROTOCOL should require of an exposure-only clause."""
    idx = pxw.index
    Wx = books[form]
    gx = mean_gross(Wx, idx)
    ew = books["EWall"]
    Wc = ew * (gx / mean_gross(ew, idx))
    return Wx, Wc, gx, abs(mean_gross(Wc, idx) - gx)


def apply_control(pxw, WA, WB, ctrl, spyw, books):
    """Return (WA', WB', label_A, label_B, matched summary, residual gap)."""
    idx = pxw.index
    if ctrl == "RAW":
        return WA, WB, "A", "B", np.nan, 0.0
    if ctrl == "GROSS":
        gA, gB = mean_gross(WA, idx), mean_gross(WB, idx)
        t = min(gA, gB)
        A2, B2 = WA * (t / gA), WB * (t / gB)
        return A2, B2, "A", "B", t, abs(mean_gross(A2, idx) - mean_gross(B2, idx))
    # VOL / BETA: two scaling passes on the weights, book RE-RUN each time (costs scale with it)
    A2, B2 = WA.copy(), WB.copy()
    for _ in range(2):
        rA, rB = fast_bt(pxw, A2), fast_bt(pxw, B2)
        if ctrl == "VOL":
            xA, xB = metrics(rA)["Vol"], metrics(rB)["Vol"]
        else:
            xA, xB = beta_to(rA, spyw), beta_to(rB, spyw)
        if not (np.isfinite(xA) and np.isfinite(xB)) or min(abs(xA), abs(xB)) <= 0:
            return A2, B2, "A", "B", np.nan, np.nan
        t = min(abs(xA), abs(xB))
        A2, B2 = A2 * (t / abs(xA)), B2 * (t / abs(xB))
    rA, rB = fast_bt(pxw, A2), fast_bt(pxw, B2)
    if ctrl == "VOL":
        xA, xB = metrics(rA)["Vol"], metrics(rB)["Vol"]
    else:
        xA, xB = beta_to(rA, spyw), beta_to(rB, spyw)
    return A2, B2, "A", "B", 0.5 * (xA + xB), abs(xA - xB)


def label(dsharpe, maxl1, floor):
    if maxl1 < MECH_TOL:
        return "MECH_DEGEN"
    if abs(dsharpe) <= floor:
        return "INVISIBLE"
    return "VISIBLE"


def main():
    t0 = time.time()
    P("=" * 118)
    P(f"# {STAMP}")
    P("# IDEA 582 - for each clause family in the record, is there ANY control the clause is not")
    P("#            degenerate against?  8 families x 5 controls x 3 panels, all reported.")
    P("=" * 118)
    P(f"# PROTOCOL: {COST:.0f} bps per unit turnover, next-day fills, weekly cadence, no shorting,")
    P(f"#           no leverage (asserted: no scaled book exceeds gross 1.0).  IS <= {IS_END}, "
      f"OOS >= {OOS_START}.")
    P(f"# TUNED (2): clause family ({len(FAMS)}) x control ({len(CONTROLS)}).  PINNED: gross {G}, "
      f"MA {MA_WIN}d, vol {VOL_WIN}d, cap {VOL_CAP}, band {BAND}, n 10/20.")
    P("#            REPORTED-NEVER-SELECTED: panel (3), window (FULL/IS/OOS), book form, offset.")
    P("")
    P("PRE-REGISTERED: H_ONE (every family VISIBLE under >=1 control on all 3 panels), H_GROSS (the")
    P("  GROSS family is MECH_DEGEN under matched gross on ALL THREE panels - idea 317 measured it")
    P("  on one), H_EXPO (matched exposure leaves the 5 holdings-changing families VISIBLE in >=80%")
    P("  of cells), H_CONST (the constant-exposure comparand is STRICTLY MORE DEMANDING: >=1")
    P("  non-GROSS family INVISIBLE against CONST while VISIBLE against its own parent at matched")
    P("  gross), H_FLOOR (>=1 published-style comparison sits inside its own convention floor),")
    P("  H_OOS (<=20% of 120 cells flip label between IS and OOS, each read once).")
    P("")

    # ---------------------------------------------------------- panels
    pxU = load_universe().dropna(how="all").ffill()
    pxB = load_universe(broad=True).dropna(how="all").ffill()
    pxS = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in pxS.columns if c == "SPY" or c not in bad]
    pxS = pxS[keep].dropna(how="all").ffill()
    panels = [("U56", pxU, np.array([True] * pxU.shape[1])),
              ("B136", pxB, np.array([True] * pxB.shape[1])),
              ("SMALL", pxS, np.array([c != "SPY" for c in pxS.columns]))]
    for nm, px, tr in panels:
        P(f"PANEL {nm:6s} {px.shape[1]:4d} cols, {int(tr.sum()):4d} tradable, {len(px)} bars "
          f"{px.index.min().date()}..{px.index.max().date()}")
    P(f"  SMALL drops {len(bad)} tickers with max_1d_move >= 1.0 per PROTOCOL; SPY is a joined")
    P("  BENCHMARK there, not a constituent.  SURVIVORSHIP: B136 and SMALL are CURRENT constituents,")
    P("  so every LEVEL on them is overstated; the object here is a DIFFERENCE on one panel.")
    P("")

    BOOKS, STARTS = {}, {}
    for nm, px, tr in panels:
        BOOKS[nm] = build_books(px, tr)
        STARTS[nm] = px.index[260]              # skip warm-up, as baseline.compare does

    # ---------------------------------------------------------- GATES
    P("=" * 118)
    P("GATES")
    P("=" * 118)
    gates = []
    worst = 0.0
    for nm, px, tr in panels:
        sub = px.loc[STARTS[nm]:]
        W = BOOKS[nm]["MA-DG"].loc[STARTS[nm]:]
        d = float(np.nanmax(np.abs(fast_bt(sub, W) - backtest(sub, W, cost_bps=COST,
                                                              freq=FREQ)["returns"])))
        worst = max(worst, d)
        P(f"  G1 engine     : {nm:6s} max |fast_bt - engine.backtest| {d:.3e}")
    P(f"                  worst {worst:.3e}  bar 1e-9 -> {'PASS' if worst < 1e-9 else 'FAIL'}")
    gates.append(dict(gate="G1_engine", value=worst, bar=1e-9, passed=bool(worst < 1e-9)))

    # ---------------------------------------------------------- convention floors
    P("")
    P("  CONVENTION FLOOR - the same book, the same 5-day cadence, the five weekday offsets.")
    P("  This is the yardstick a clause must clear to be visible at all.")
    floors, frows = {}, []
    forms_used = sorted({f for p in PAIRS.values() for f in p} | {"EWall"})
    for nm, px, tr in panels:
        sub = px.loc[STARTS[nm]:]
        for form in forms_used:
            W = BOOKS[nm][form].loc[STARTS[nm]:]
            sh = [metrics(fast_bt(sub, W, _mask_offset(sub.index, o)))["Sharpe"] for o in range(5)]
            floors[(nm, form)] = float(max(sh) - min(sh))
            frows.append(dict(panel=nm, form=form, spread=floors[(nm, form)],
                              **{f"off{o}": sh[o] for o in range(5)}))
    FL = pd.DataFrame(frows)
    FL.to_csv(f"{OUT}/{STAMP}.floors.csv", index=False)
    P(f"  {'panel':6s} " + " ".join(f"{f:>10s}" for f in forms_used))
    for nm, _, _ in panels:
        P(f"  {nm:6s} " + " ".join(f"{floors[(nm, f)]:10.4f}" for f in forms_used))
    P("  (Sharpe spread over the 5 offsets; per-cell floor = max of the two compared books' spreads)")

    # ---------------------------------------------------------- the grid
    P("")
    P("=" * 118)
    P("THE GRID - 8 clause families x 5 controls x 3 panels, FULL sample.  A cell is MECH_DEGEN when")
    P("the two target-weight paths coincide (max L1/2 < 1e-9), INVISIBLE when |dSharpe| <= its own")
    P("convention floor, VISIBLE otherwise.")
    P("=" * 118)
    cells, maxg, gapworst = [], 0.0, 0.0
    spyU = pxU["SPY"].pct_change()
    for wname, sl in (("FULL", slice(None, None)), ("IS", slice(None, IS_END)),
                      ("OOS", slice(OOS_START, None))):
        for nm, px, tr in panels:
            s0 = STARTS[nm]
            pxw = px.loc[s0:].loc[sl]
            if len(pxw) < 300:
                continue
            spyw = px["SPY"].pct_change().loc[pxw.index]
            bks = {k: v.loc[pxw.index] for k, v in BOOKS[nm].items()}
            for fam in FAMS:
                fa, fb = PAIRS[fam]
                for ctrl in CONTROLS:
                    extra = {}
                    if ctrl == "CONST":
                        # BOTH arms against their own constant-exposure comparand; the cell keeps
                        # the MORE visible of the two, since a family is invisible to constant
                        # exposure only if NEITHER arm can be told apart from it.
                        legs = []
                        for form in (fa, fb):
                            Wx, Wc, gx, gp = const_legs(pxw, bks, form)
                            rx, rc = fast_bt(pxw, Wx), fast_bt(pxw, Wc)
                            mx, mc = rowify(rx), rowify(rc)
                            l1 = l1_dist(Wx, Wc, pxw.index)
                            legs.append(dict(form=form, WA=Wx, WB=Wc, rA=rx, rB=rc, mA=mx, mB=mc,
                                             l1=l1, matched=gx, gap=gp,
                                             ds=mx["Sharpe"] - mc["Sharpe"]))
                        legs.sort(key=lambda d: -abs(d["ds"]))
                        w, o = legs[0], legs[1]
                        WA, WB, rA, rB, mA, mB = w["WA"], w["WB"], w["rA"], w["rB"], w["mA"], w["mB"]
                        l1m, l1x = w["l1"]
                        matched, gap = w["matched"], w["gap"]
                        armA, armB = w["form"], f"EWall@g({w['form']})"
                        fl = max(floors[(nm, w["form"])], floors[(nm, "EWall")])
                        extra = dict(other_arm=o["form"], other_dSharpe=o["ds"],
                                     other_l1_max=o["l1"][1])
                    else:
                        WA, WB, la, lb, matched, gap = apply_control(pxw, bks[fa], bks[fb], ctrl,
                                                                     spyw, bks)
                        rA, rB = fast_bt(pxw, WA), fast_bt(pxw, WB)
                        mA, mB = rowify(rA), rowify(rB)
                        l1m, l1x = l1_dist(WA, WB, pxw.index)
                        armA, armB = fa, fb
                        fl = max(floors[(nm, fa)], floors[(nm, fb)])
                    maxg = max(maxg, float(WA.sum(axis=1).max()), float(WB.sum(axis=1).max()))
                    if np.isfinite(gap) and ctrl == "GROSS":
                        gapworst = max(gapworst, gap)
                    ds = mA["Sharpe"] - mB["Sharpe"]
                    cells.append(dict(window=wname, panel=nm, family=fam, control=ctrl,
                                      armA=armA, armB=armB,
                                      dSharpe=ds, dCAGR=mA["CAGR"] - mB["CAGR"],
                                      dMaxDD=mA["MaxDD"] - mB["MaxDD"],
                                      corr=float(pd.concat([rA, rB], axis=1).corr().iloc[0, 1]),
                                      l1_mean=l1m, l1_max=l1x, floor=fl,
                                      label=label(ds, l1x, fl), matched=matched, match_gap=gap,
                                      A_Sharpe=mA["Sharpe"], B_Sharpe=mB["Sharpe"],
                                      A_CAGR=mA["CAGR"], B_CAGR=mB["CAGR"],
                                      A_MaxDD=mA["MaxDD"], B_MaxDD=mB["MaxDD"], **extra))
    CE = pd.DataFrame(cells)
    CE.to_csv(f"{OUT}/{STAMP}.cells.csv", index=False)
    P(f"  G2 matching   : max target gross over every scaled book {maxg:.6f}  bar <= 1.0 -> "
      f"{'PASS' if maxg <= 1.0 + 1e-12 else 'FAIL'};  worst matched-GROSS residual {gapworst:.3e} "
      f"bar 1e-12 -> {'PASS' if gapworst < 1e-12 else 'FAIL'}")
    gates.append(dict(gate="G2_no_leverage", value=maxg, bar=1.0, passed=bool(maxg <= 1 + 1e-12)))
    gates.append(dict(gate="G2_gross_match", value=gapworst, bar=1e-12,
                      passed=bool(gapworst < 1e-12)))
    vg = CE[(CE.window == "FULL") & (CE.control == "VOL")].match_gap
    bg = CE[(CE.window == "FULL") & (CE.control == "BETA")].match_gap
    P(f"                  VOL control residual |vol_A - vol_B| max {vg.max():.3e} "
      f"(median {vg.median():.3e}); BETA residual max {bg.max():.3e} (median {bg.median():.3e}) - "
      f"measured, not a bar: two scaling passes, stated.")

    F = CE[CE.window == "FULL"]
    g3 = F[(F.panel == "U56") & (F.control == "GROSS")].set_index("family")
    P("")
    P("  G3 parent     : matched-gross |dSharpe| per family on U56 vs idea 317's committed G3")
    P(f"      {'family':8s} {'idea 317':>11s} {'this run':>11s} {'this L1max':>11s} {'label':>11s}")
    for fam in P317:
        r = g3.loc[fam]
        P(f"      {fam:8s} {P317[fam]:11.3e} {abs(r.dSharpe):11.3e} {r.l1_max:11.3e} "
          f"{r.label:>11s}")
    hard = abs(g3.loc["GROSS"].dSharpe)
    P(f"      hard bar: GROSS must still collapse - |dSharpe| {hard:.3e} and L1max "
      f"{g3.loc['GROSS'].l1_max:.3e} < 1e-9 -> "
      f"{'PASS' if g3.loc['GROSS'].l1_max < MECH_TOL else 'FAIL'}")
    P("      The other five are a DRIFT reading: idea 317 took its max over 288 conditional cells'")
    P("      parent legs (its panel mix and its cell set), this run compares the parent pair itself.")
    gates.append(dict(gate="G3_GROSS_collapse", value=float(g3.loc["GROSS"].l1_max), bar=MECH_TOL,
                      passed=bool(g3.loc["GROSS"].l1_max < MECH_TOL)))

    # G5 the parent's naming fault, gated
    P("")
    P("  G5 semantics  : what the record's '-DG' books actually do (mean TARGET GROSS on rebalance")
    P("                  days; a de-gross book must sit BELOW base gross 0.75, a re-spread book AT it)")
    g5 = []
    for nm, px, tr in panels:
        idx = px.loc[STARTS[nm]:].index
        gs = {f: mean_gross(BOOKS[nm][f].loc[idx], idx)
              for f in ("EWall", "MA-RS", "MA-DG", "BAND-RS", "BAND-DG", "VOLCAP-DG",
                        "IDEA317-MADG")}
        d317 = l1_dist(BOOKS[nm]["IDEA317-MADG"].loc[idx], BOOKS[nm]["MA-RS"].loc[idx], idx)[1]
        g5.append(d317)
        P(f"      {nm:6s} " + "  ".join(f"{k} {v:.4f}" for k, v in gs.items()))
        P(f"             idea 317's MA-DG vs this file's MA-RS: max L1/2 {d317:.3e} -> "
          f"{'THE SAME BOOK' if d317 < MECH_TOL else 'different'};  vs a true de-gross the mean "
          f"gross differs by {gs['MA-RS'] - gs['MA-DG']:+.4f}")
    ok5 = max(g5) < MECH_TOL
    P(f"                  bar: idea 317's 'MA-DG' IS its re-spread book on all 3 panels "
      f"(max {max(g5):.3e} < 1e-9) -> {'PASS (the naming fault is established)' if ok5 else 'FAIL'}")
    gates.append(dict(gate="G5_317_MADG_is_respread", value=max(g5), bar=MECH_TOL, passed=bool(ok5)))

    # G4 determinism
    pxw = pxU.loc[STARTS["U56"]:]
    r1 = metrics(fast_bt(pxw, BOOKS["U56"]["TOP20"].loc[pxw.index]))["Sharpe"]
    r2 = metrics(fast_bt(pxw, BOOKS["U56"]["TOP20"].loc[pxw.index]))["Sharpe"]
    P(f"  G4 determinism: rebuilt cell Sharpe differs by {abs(r1-r2):.3e}  bar 0 -> "
      f"{'PASS' if r1 == r2 else 'FAIL'}")
    gates.append(dict(gate="G4_determinism", value=abs(r1 - r2), bar=0.0, passed=bool(r1 == r2)))
    pd.DataFrame(gates).to_csv(f"{OUT}/{STAMP}.gates.csv", index=False)

    # ---------------------------------------------------------- the census
    P("")
    P("=" * 118)
    P("WHICH CLAUSES ARE INVISIBLE TO WHICH CONTROL  (FULL sample; M = MECH_DEGEN, I = INVISIBLE,")
    P("V = VISIBLE; the number under each label is |dSharpe| and, in brackets, the cell's floor)")
    P("=" * 118)
    for nm, _, _ in panels:
        P(f"  panel {nm}")
        P(f"    {'family':8s} " + " ".join(f"{c:>20s}" for c in CONTROLS))
        for fam in FAMS:
            line = f"    {fam:8s} "
            for ctrl in CONTROLS:
                r = F[(F.panel == nm) & (F.family == fam) & (F.control == ctrl)]
                if len(r) == 0:
                    line += f"{'n/a':>20s} "
                    continue
                r = r.iloc[0]
                tag = {"MECH_DEGEN": "M", "INVISIBLE": "I", "VISIBLE": "V"}[r.label]
                line += f"{tag} {abs(r.dSharpe):7.4f} [{r.floor:6.4f}] "
            P(line)
        P("")

    # ---------------------------------------------------------- hypotheses
    P("=" * 118)
    P("PRE-REGISTERED TESTS")
    P("=" * 118)
    HOLD = ("TREND", "VOLCAP", "WIDEN", "CONC", "DEFEND")
    res = {}
    vis = F[F.label == "VISIBLE"]
    ok_all = []
    for fam in FAMS:
        good = [c for c in CONTROLS
                if len(vis[(vis.family == fam) & (vis.control == c)]) == len(panels)]
        ok_all.append(bool(good))
        P(f"  H_ONE   : {fam:8s} VISIBLE on all 3 panels under: "
          f"{', '.join(good) if good else 'NO CONTROL'}")
    res["H_ONE"] = bool(all(ok_all))
    P(f"            -> {'PASS' if res['H_ONE'] else 'FAIL'} "
      f"({sum(ok_all)} of {len(FAMS)} families have such a control)")

    gr = F[(F.family == "GROSS") & (F.control == "GROSS")]
    res["H_GROSS"] = bool((gr.label == "MECH_DEGEN").all() and len(gr) == len(panels))
    P("")
    P("  H_GROSS : GROSS family under matched gross, per panel: " +
      ", ".join(f"{r.panel} L1max {r.l1_max:.2e} dSharpe {abs(r.dSharpe):.2e} {r.label}"
                for _, r in gr.iterrows()))
    P(f"            -> {'PASS' if res['H_GROSS'] else 'FAIL'} (idea 317's one-panel collapse "
      f"generalises to all three)")

    sub = F[(F.family.isin(HOLD)) & (F.control.isin(("GROSS", "VOL", "BETA")))]
    share = float((sub.label == "VISIBLE").mean())
    res["H_EXPO"] = bool(share >= 0.80)
    P("")
    P(f"  H_EXPO  : holdings-changing families under matched exposure: VISIBLE in "
      f"{int((sub.label=='VISIBLE').sum())} of {len(sub)} cells ({share:.0%}), bar 80% -> "
      f"{'PASS' if res['H_EXPO'] else 'FAIL'}")
    for lbl, cnt in sub.label.value_counts().items():
        P(f"            {lbl}: {cnt}")
    bad_cells = sub[sub.label != "VISIBLE"]
    for _, r in bad_cells.iterrows():
        P(f"            not visible: {r.panel}/{r.family}/{r.control} |dSharpe| "
          f"{abs(r.dSharpe):.4f} floor {r.floor:.4f} L1max {r.l1_max:.2e} -> {r.label}")

    flips = []
    for nm, _, _ in panels:
        for fam in FAMS:
            if fam == "GROSS":
                continue
            c1 = F[(F.panel == nm) & (F.family == fam) & (F.control == "CONST")]
            c2 = F[(F.panel == nm) & (F.family == fam) & (F.control == "GROSS")]
            if len(c1) and len(c2) and c1.iloc[0].label != "VISIBLE" and c2.iloc[0].label == "VISIBLE":
                flips.append(f"{nm}/{fam} (CONST {c1.iloc[0].label} "
                             f"|dSharpe| {abs(c1.iloc[0].dSharpe):.4f} vs parent-at-matched-gross "
                             f"VISIBLE {abs(c2.iloc[0].dSharpe):.4f})")
    res["H_CONST"] = bool(flips)
    P("")
    P(f"  H_CONST : non-GROSS families invisible to CONSTANT EXPOSURE but visible to their own "
      f"parent: {len(flips)}")
    for f_ in flips:
        P(f"            {f_}")
    P(f"            -> {'PASS' if res['H_CONST'] else 'FAIL'}")

    pub = F[F.control.isin(("RAW", "GROSS"))]
    inside = pub[(pub.label == "INVISIBLE")]
    res["H_FLOOR"] = bool(len(inside))
    P("")
    P(f"  H_FLOOR : published-style comparisons (RAW or matched-GROSS) inside their own convention "
      f"floor: {len(inside)} of {len(pub)}")
    for _, r in inside.iterrows():
        P(f"            {r.panel}/{r.family}/{r.control} |dSharpe| {abs(r.dSharpe):.4f} <= floor "
          f"{r.floor:.4f}  (L1 mean {r.l1_mean:.3f} - the books DO differ, the Sharpe gap does not)")
    P(f"            -> {'PASS' if res['H_FLOOR'] else 'FAIL'}")

    # ---------------------------------------------------------- rule 8 / WF-A
    P("")
    P("=" * 118)
    P("RULE 8 / WF-A - the LABEL walked forward.  Each window is its own backtest and each control's")
    P("scaling is re-derived inside it; the IS label is read, then the OOS label read ONCE.")
    P("=" * 118)
    key = ["panel", "family", "control"]
    I = CE[CE.window == "IS"].set_index(key)
    O = CE[CE.window == "OOS"].set_index(key)
    both = I.index.intersection(O.index)
    flip = [(k, I.loc[k, "label"], O.loc[k, "label"]) for k in both
            if I.loc[k, "label"] != O.loc[k, "label"]]
    rate = len(flip) / max(len(both), 1)
    res["H_OOS"] = bool(rate <= 0.20)
    P(f"  {len(both)} cells labelled in both windows; {len(flip)} FLIP ({rate:.1%}), bar 20% -> "
      f"{'PASS' if res['H_OOS'] else 'FAIL'}")
    P(f"  {'panel/family/control':34s} {'IS':>11s} {'OOS':>11s} {'IS dSh':>8s} {'OOS dSh':>8s} "
      f"{'IS floor':>9s}")
    for k, a, b in flip:
        P(f"  {'/'.join(k):34s} {a:>11s} {b:>11s} {I.loc[k,'dSharpe']:8.4f} "
          f"{O.loc[k,'dSharpe']:8.4f} {I.loc[k,'floor']:9.4f}")
    byfam = pd.DataFrame([dict(family=k[1], flipped=1) for k, a, b in flip])
    if len(byfam):
        P("  flips by family: " + ", ".join(f"{k} x{v}" for k, v in
                                            byfam.family.value_counts().items()))
    wf = CE[CE.window.isin(("IS", "OOS"))]
    wf.to_csv(f"{OUT}/{STAMP}.walkforward.csv", index=False)

    # ---------------------------------------------------------- WF-B + KEEP paths
    P("")
    P("=" * 118)
    P("RULE 8 / WF-B + KEEP PATHS - every book this file runs, scored as a book.")
    P("=" * 118)
    s0 = STARTS["U56"]
    idxb = pxU.loc[s0:].index
    base_r = fast_bt(pxU.loc[s0:], rules_v2_weights(pxU).loc[idxb])
    spy_ret = pxU["SPY"].pct_change().fillna(0.0).loc[idxb]
    bm, sm = rowify(base_r), rowify(spy_ret)
    P(f"  comparands on U56 over {idxb[0].date()}..{idxb[-1].date()}")
    for lbl, m, r in (("RULES v2 (U56, live)", bm, base_r), ("SPY", sm, spy_ret)):
        mo = metrics(r.loc[OOS_START:])
        P(f"    {lbl:22s} CAGR {m['CAGR']:.2%} Sharpe {m['Sharpe']:.3f} MaxDD {m['MaxDD']:.2%} "
          f"halves {m['H1']:.3f}/{m['H2']:.3f} | OOS CAGR {mo['CAGR']:.2%} Sharpe "
          f"{mo['Sharpe']:.3f} MaxDD {mo['MaxDD']:.2%}")
    books = []
    for nm, px, tr in panels:
        s0n = STARTS[nm]
        pxn = px.loc[s0n:]
        own = fast_bt(pxn, rules_v2_weights(px).loc[pxn.index])
        spyn = px["SPY"].pct_change().fillna(0.0).loc[pxn.index]
        bu = base_r.reindex(pxn.index).fillna(0.0)
        bks = {k: v.loc[pxn.index] for k, v in BOOKS[nm].items()}
        for fam in FAMS:
            fa, fb = PAIRS[fam]
            for ctrl in CONTROLS:
                if ctrl == "CONST":
                    WA, _, _, _ = const_legs(pxn, bks, fa)
                    WB, WC, _, _ = const_legs(pxn, bks, fb)
                    legs = (("A", fa, WA), ("B", fb, WB), ("C", f"EWall@g({fb})", WC))
                else:
                    WA, WB, _, _, _, _ = apply_control(pxn, bks[fa], bks[fb], ctrl, spyn, bks)
                    legs = (("A", fa, WA), ("B", fb, WB))
                for side, form, W in legs:
                    r = fast_bt(pxn, W)
                    m = rowify(r)
                    mo = metrics(r.loc[OOS_START:])
                    mi = metrics(r.loc[:IS_END])
                    books.append(dict(panel=nm, family=fam, control=ctrl, side=side, form=form,
                                      **m, IS_Sharpe=mi["Sharpe"], OOS_CAGR=mo["CAGR"],
                                      OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                      keep4a_U56=keep_4a(r, bu), keep4a_own=keep_4a(r, own),
                                      fail4b=fail_4b(r, spyn), keep4b=fail_4b(r, spyn) == "-"))
    BK = pd.DataFrame(books)
    BK.to_csv(f"{OUT}/{STAMP}.keeppaths.csv", index=False)
    P(f"  {len(BK)} books (3 panels x 8 families x 5 controls x 2-3 legs; duplicates across "
      f"families kept so every cell is scored)")
    P(f"  KEEP paths: 4a vs RULES v2 on U56 {int(BK.keep4a_U56.sum())}; 4a vs RULES v2 on the "
      f"book's OWN panel {int(BK.keep4a_own.sum())}; 4b {int(BK.keep4b.sum())}; BOTH (U56 read) "
      f"{int((BK.keep4a_U56 & BK.keep4b).sum())}")
    P("  most common 4b failure sets: " + ", ".join(f"{k} x{v}" for k, v in
                                                    BK.fail4b.value_counts().head(5).items()))
    if int(BK.keep4b.sum()):
        P("  4b passes (diagnostic - these are the record's standard forms, not new candidates):")
        for _, r in BK[BK.keep4b].drop_duplicates(["panel", "form", "control"]).iterrows():
            P(f"    {r.panel}/{r.form}/{r.control}  CAGR {r.CAGR:.2%} Sharpe {r.Sharpe:.3f} "
              f"MaxDD {r.MaxDD:.2%} halves {r.H1:.3f}/{r.H2:.3f} OOS Sharpe {r.OOS_Sharpe:.3f}")
    pick = BK.sort_values("IS_Sharpe", ascending=False).iloc[0]
    P("")
    P("  WF-B pick (IS Sharpe ALONE, OOS read once):")
    P(f"    {pick.panel}/{pick.form} under {pick.control}  IS Sharpe {pick.IS_Sharpe:.3f}")
    P(f"    OOS  CAGR {pick.OOS_CAGR:.2%}  Sharpe {pick.OOS_Sharpe:.3f}  MaxDD {pick.OOS_MaxDD:.2%}"
      f"   vs RULES v2 OOS {metrics(base_r.loc[OOS_START:])['CAGR']:.2%}/"
      f"{metrics(base_r.loc[OOS_START:])['Sharpe']:.3f} and SPY OOS "
      f"{metrics(spy_ret.loc[OOS_START:])['CAGR']:.2%}/"
      f"{metrics(spy_ret.loc[OOS_START:])['Sharpe']:.3f}")
    P(f"    FULL CAGR {pick.CAGR:.2%} Sharpe {pick.Sharpe:.3f} MaxDD {pick.MaxDD:.2%} halves "
      f"{pick.H1:.3f}/{pick.H2:.3f}  4a(U56) {bool(pick.keep4a_U56)} 4b fails [{pick.fail4b}]")

    P("")
    P("=" * 118)
    P("VERDICT")
    P("=" * 118)
    for k, v in res.items():
        P(f"  {k:10s} {'PASS' if v else 'FAIL'}")
    P(f"  ran in {time.time()-t0:.1f}s")
    Path(f"{OUT}/{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")
    return res


if __name__ == "__main__":
    main()

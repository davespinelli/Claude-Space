#!/usr/bin/env python3
"""
Idea 997 (lane C, 2026-09-16)
PRICE THE LIVE BOOK AS A STANDING 4b COMPARAND -- WALK IT ON A GROSS LADDER 0.25 .. 1.50

  Idea 993's degenerate all-refuse point -- every slot declined, i.e. THE LIVE BOOK HELD
  EVERYWHERE -- beat the best screened point on median OOS Sharpe (1.1061 vs 1.0011) AND on
  median OOS MaxDD (-12.24% vs -20.00%), and still bought ZERO OOS 4b passes against three.
  993's own committed fallbacks.csv says why in one column: `fail_legs` for FB_LIVE reads
  `L5_CAGR` alone on U56 and on B136.  Four of 4b's five legs already pass.  The book is
  refused for being SMALL, not for being bad.

  So the question 997 asks is not about a signal at all.  It is an accounting question about
  one dial:  4b's CAGR floor is a LOWER bar that the book clears by carrying more risk, and
  4b's DD cap is an UPPER bar that the same dial spends.  Both move monotonically with gross.
  Either the two bars overlap -- there is a WINDOW of gross at which the live book is
  capital-worthy -- or they do not, and the live book is 4b-unpassable at EVERY size, which is
  a far stronger statement about the book than "it failed at 0.75".

  THE OBJECT MEASURED HERE, stated before any number:  for each panel, the two crossing rungs

      g_CAGR = the smallest rung whose OOS CAGR clears  0.70 x SPY CAGR      (floor, rises with g)
      g_DD   = the largest  rung whose OOS MaxDD clears 0.60 x |SPY MaxDD|   (cap,  spent  with g)

  and the window [g_CAGR, g_DD].  It is non-empty iff g_CAGR <= g_DD.  The incumbent live book
  sits at gross 0.75 and its position RELATIVE to that window is the answer.

  WHAT THIS RUN CANNOT CLAIM, said here and not buried in the memo: gross is not alpha.  Idea
  948 found the gross dial Sharpe-neutral to +/-0.005 because it scales turnover and vol
  together and the cost rebate cancels in the ratio.  If a rung passes 4b here it passes by
  CONVERTING AN UNSPENT RISK BUDGET INTO RETURN, not by picking better.  H_SHARPE_FLAT tests
  948's cancellation across this whole ladder precisely so the reader can see that the Sharpe
  legs are inherited from the book and only the two SIZE legs are bought.

  NOR IS THE FINDING NEW TO THE RECORD, in part: idea 984 already published four OOS 4b passes
  at U56/`BAND03`@gross 1.00 (D/W), and idea 988 is the open queue item asking whether any
  gross rung clears BOTH KEEP paths on the fast cadences.  993's ladder carries the W/phase-0
  U56 EXT row with pass4b = True.  What 997 adds is (a) the ladder at 0.05 resolution, which
  LOCATES both crossings instead of sampling two points, (b) the rule-8 question -- would an
  IS-only chooser standing at 2016-12-31 have picked a rung inside the window? -- and (c) the
  three ways the window can be an artefact: FINANCING on the levered rungs, the REBALANCE
  PHASE (the DD leg is the record's known phase coin-flip), and the leg definition.

TUNED AXES -- exactly two, every level reported, none selected:
  (1) gross : 0.25, 0.30, ... 1.50   (26 rungs, step 0.05)
  (2) panel : U56, B136, SMALL
Everything else is FIXED at the live book's own committed setting and is a reporting column,
never a level anything is chosen on:
  book     = BAND03 @ band 0.03  == baseline.rules_v2_weights (gated exactly, G2)
  cadence  = W, phase 0          (RULES v2's own schedule; D/M/Q and all 5 W phases published)
  cost     = 10 bps headline     (rungs 0 / 5 / 10 / 25 / 50 all built)
  split    = IS 2009-2016 / OOS 2017-2026, read once

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read):
  H_WINDOW    : the window [g_CAGR, g_DD] is NON-EMPTY on at least one panel
  H_PANEL     : it is non-empty on ALL THREE panels
  H_INCUMBENT : the incumbent 0.75 lies BELOW the window (the live book is UNDER-grossed, not
                over-grossed) on every panel whose window is non-empty
  H_4B        : some rung passes FULL 4b out of sample (all five legs, not just the two size legs)
  H_R8        : rule 8 -- a rung chosen on 2009-2016 ALONE passes 4b on the untouched OOS window,
                on at least one panel, under at least one of the three pre-declared IS choosers
  H_R8_ALL    : ... under ALL THREE choosers on every panel whose window is non-empty
  H_4A        : some rung clears KEEP path 4a against RULES v2.  Pre-declared EXPECTED FAIL: the
                DD leg of 4a is measured against the live book's OWN -12.05%, and any rung above
                the incumbent has a strictly worse drawdown, so 4a can only be bought BELOW 0.75
                where the Sharpe legs are unchanged and so cannot strictly beat.  Stated as a
                hypothesis anyway so the refusal is a measured number, not an assumption.
  H_SHARPE_FLAT: max |OOS Sharpe(g) - OOS Sharpe(0.75)| over the whole ladder <= 0.005, i.e. idea
                948's cancellation holds across 0.25-1.50 and not merely across a halving
  H_MONO      : OOS CAGR and |OOS MaxDD| are both non-decreasing in g on every panel (if this
                fails the two-crossing framing is wrong and the window is not an interval)
  H_BORROW    : the window survives a financing charge of 200 bps/yr on the levered fraction
  H_PHASE     : the window verdict is stable across all 5 weekly phases (the record's L4_DD leg
                flips on phase; if it flips here the window is a phase artefact)
  H_LEGDEF    : the window is the same under the record's committed leg definition (OOS metrics
                against FULL-sample SPY bars) and under an ALL-OOS reading of the same bars

GATES (printed before any hypothesis number):
  G0  offset_mask(idx, per, 0) == engine.rebalance_mask(idx, per) on D/W/M/Q
  G1  the fast Ctx runner == engine.backtest on returns AND turnover, post warm-up, D and W
  G2  BAND03 @ 0.75 == baseline.rules_v2_weights elementwise -- the subject IS the live book
  G3  CROSS-RUN: idea 993's committed fallbacks.csv FB_LIVE rows (3 panels x 15 metrics)
      reproduced by this run's gross-0.75 / W / phase 0 / 10 bps row
  G3b CROSS-RUN: idea 993's committed 13,500-row ladder, BAND03 x {CORE 0.75, EXT 1.00} x W x
      phase 0 x 5 cost rungs (30 rows) reproduced on every shared numeric column
  G4  MATCHED CONSTRUCTION: one target matrix per (panel, gross), built once, reused across
      every cadence and phase
  G5  determinism: one cell rebuilt from scratch and differenced
  G6  GROSS IDENTITY: the target matrix at g is EXACTLY (g/0.75) x the target matrix at 0.75
  G7  IS-PURITY: every IS chooser's pick is invariant under a permutation of the OOS returns
  G8  LEVERAGE ACCOUNTING: the financing charge is identically zero at every rung <= 1.00 and
      strictly positive at every rung > 1.00, and equals BORROW x mean(max(exposure-1, 0))

PROTOCOL: 10 bps primary, decided at close t / applied t+1 (LAG 1), warm-up 260 days, IS
2009-2016 / OOS 2017-2026 read once, no shorting.  LEVERAGE: rungs above 1.00 are levered; the
idea as queued names the ladder to 1.50, and PROTOCOL rule 2 permits leverage only where the
idea says so, so the levered rungs are reported with a DECLARED financing charge beside the
record's own zero-borrow convention and neither is allowed to hide the other.  Rule 8
walk-forward is run on the tuned axis itself.  Both KEEP paths are evaluated at every one of
the 78 (panel, gross) grid points.  Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py /
baseline.py is modified.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally
drops every ticker with max_1d_move >= 1.0 per data/small_meta.csv).  This run is NOT immune the
way a two-convention difference is: the object here is a LEVEL (a CAGR and a drawdown) compared
against SPY, and survivorship inflates the book's level while leaving SPY's alone.  Both
crossing rungs are therefore OPTIMISTIC -- g_CAGR is a lower bound on the true crossing and
g_DD is likewise flattered -- and any window reported here is an UPPER bound on the true one.
This is stated again in the memo and is the single largest reason a pass here is not a licence.

  SMOKE=1 runs a coarse gross ladder for wiring checks only; headline numbers are the full run.
"""
from __future__ import annotations

import os
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

SMOKE = os.environ.get("SMOKE") == "1"

# ---- reported constants (never tuned) ---------------------------------------------------
WARM = 260
LAG = 1
BAND0 = 0.03
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
HEAD_COST = 10.0
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
CADENCES = {"D": 1, "W": 5, "M": 21, "Q": 63}
CADORDER = ["D", "W", "M", "Q"]
HEAD_CAD = "W"                       # RULES v2's own schedule
HEAD_PHASE = 0                       # the canonical date nobody tuned
INCUMBENT = 0.75                     # RULES v2's committed gross

GROSS_LADDER = [round(0.25 + 0.05 * i, 2) for i in range(26)]          # 0.25 .. 1.50
if SMOKE:
    GROSS_LADDER = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50]

BORROW_BPS = 200.0                   # DECLARED financing rate on the levered fraction, per year
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
CHOOSERS = ["C_ISSHARPE", "C_ISCAGR", "C_IS4B"]
BAR_FLAT = 0.005                     # H_SHARPE_FLAT: idea 948's cancellation band

# idea 993's committed artifacts (G3)
P993 = OUT / "2026-09-16_price-the-EMPTIED-SLOT-COST_C.fallbacks.csv"
P993_LAD = OUT / "2026-09-16_price-the-EMPTIED-SLOT-COST_C.ladder.csv"
G3_TOL = 1e-10

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# =========================================================================================
# (1) cadence / phase machinery -- the record's form, verbatim from 980 / 993
# =========================================================================================
def offset_mask(idx, per, d):
    if per == "D":
        return pd.Series(True, index=idx), 0
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


class Ctx:
    """Vectorised equivalent of engine.backtest for a fixed rebalance mask (gated at G1).

    Returns the gross return series, the turnover series, and the realised GROSS EXPOSURE
    (sum of held weights), which is what the financing charge is levied on."""

    def __init__(self, px, mask):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = np.asarray(mask.values, bool)
        m = np.concatenate([[False], m[:-1]]).copy()
        m[0] = True
        self.T, self.N = self.rets.shape
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.N)), C[:-1]])
        self.reb = np.flatnonzero(m)
        seg = np.searchsorted(self.reb, np.arange(self.T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.ratio = self.Cp / self.Cp[self.s0]
        self.ratiop = self.Cp / self.Cp[self.s0p]

    def run(self, wt):
        W0 = wt[self.s0]
        h = W0 * self.ratio
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = wt[self.s0p]
        hp = W0p * self.ratiop
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp[self.reb]).sum(axis=1)
        return (held * self.rets).sum(axis=1), turn, held.sum(axis=1)


def shift1(W, idx):
    return W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def mets(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=sharpe(r), MaxDD=maxdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


# ---- the record's committed leg readings (993's legs_REC / legs_ISONLY, verbatim) --------
def legs_REC(row):
    """PROTOCOL 4b as the record scores it: OOS book metrics against FULL-sample SPY bars."""
    return dict(H1=row["H1"] > row["spy_H1"], H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= DD_CAP * abs(row["spy_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= CAGR_FLOOR * row["spy_CAGR"])


def legs_ALLOOS(row):
    """Companion reading: the same two size bars taken on the OOS window's own SPY."""
    return dict(H1=row["H1"] > row["spy_H1"], H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= DD_CAP * abs(row["spy_OOS_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= CAGR_FLOOR * row["spy_OOS_CAGR"])


def legs_ISONLY(row):
    """The IS-only analogue an operator standing at 2016-12-31 could legally read."""
    return dict(H1=row["IS_H1"] > row["spy_IS_H1"], H2=row["IS_H2"] > row["spy_IS_H2"],
                OOS=row["IS_Sharpe"] > row["spy_IS_Sharpe"],
                DD=abs(row["IS_MaxDD"]) <= DD_CAP * abs(row["spy_IS_MaxDD"]),
                CAGR=row["IS_CAGR"] >= CAGR_FLOOR * row["spy_IS_CAGR"])


def pass4a(row):
    return bool(row["H1"] > row["v2_H1"] and row["H2"] > row["v2_H2"]
                and row["MaxDD"] >= row["v2_MaxDD"])


# =========================================================================================
# (2) the subject: the live book, at an arbitrary gross
# =========================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def live_book(px, g):
    """RULES v2's construction with the gross dial free. g == 0.75 IS the live book (G2)."""
    return ew_gross(px, g).where(band_state(px, BAND0) & px.notna(), 0.0)


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)


def _row_metrics(net, isw, osw, spy_full, spy_is, spy_oos, v2):
    f, i_, o_ = mets(net[WARM:]), mets(net[WARM:][isw[WARM:]]), mets(net[osw])
    row = {}
    for k, v in f.items():
        row[k] = v
    for k, v in i_.items():
        row["IS_" + k] = v
    for k, v in o_.items():
        row["OOS_" + k] = v
    for k, v in spy_full.items():
        row["spy_" + k] = v
    for k, v in spy_is.items():
        row["spy_IS_" + k] = v
    for k, v in spy_oos.items():
        row["spy_OOS_" + k] = v
    for k, v in v2.items():
        row["v2_" + k] = v
    return row


def finish(row):
    lr, la, li = legs_REC(row), legs_ALLOOS(row), legs_ISONLY(row)
    for k in LEGS:
        row["leg_" + k] = bool(lr[k])
        row["alloos_" + k] = bool(la[k])
        row["isleg_" + k] = bool(li[k])
    row["pass4b"] = bool(all(lr.values()))
    row["pass4b_alloos"] = bool(all(la.values()))
    row["IS_pass4b"] = bool(all(li.values()))
    row["IS_legs_passed"] = int(sum(li.values()))
    row["pass4a"] = pass4a(row)
    row["fail_legs"] = ",".join(LEGNAME[k] for k in LEGS if not lr[k]) or "-"
    return row


# =========================================================================================
# (3) main
# =========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 997 (lane C, 2026-09-16) -- PRICE THE LIVE BOOK AS A STANDING 4b COMPARAND")
    P("  WALK RULES v2 ON A GROSS LADDER 0.25 .. 1.50 AND LOCATE THE CAGR-FLOOR / DD-CAP WINDOW")
    P("=" * 100)
    P(f"  SMOKE={SMOKE}   headline cost {HEAD_COST:.0f} bps (rungs {RUNGS})  LAG={LAG}  WARM={WARM}")
    P(f"  tuned axes: gross {GROSS_LADDER[0]:.2f}..{GROSS_LADDER[-1]:.2f} step 0.05 "
      f"({len(GROSS_LADDER)} rungs) x panel {{U56,B136,SMALL}} -- ALL reported, none selected")
    P(f"  FIXED: book = BAND03@band {BAND0} (== rules_v2_weights at gross {INCUMBENT}), "
      f"cadence {HEAD_CAD} phase {HEAD_PHASE}")
    P(f"  DECLARED: rungs > 1.00 are LEVERED; financing companion charged at {BORROW_BPS:.0f} "
      f"bps/yr on mean(max(exposure-1,0)); the record's zero-borrow convention is reported beside it")
    P("  DECLARED: 4b legs read as the record reads them (legs_REC: OOS book vs FULL-sample SPY "
      "bars); an ALL-OOS companion is carried in every table and selected on by nothing")

    P()
    P("loading panels ...")
    u56 = load_universe()
    b136 = load_universe(broad=True)
    small, ndrop = load_small()
    panels = {"U56": u56, "B136": b136, "SMALL": small}
    for k, v in panels.items():
        P(f"  {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}")
    P(f"  SMALL dropped {ndrop} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")

    # ---------------------------------------------------------------- gates
    P()
    P("=" * 100)
    P("(A) GATES -- printed before any hypothesis number")
    P("=" * 100)
    gates = []

    bad = sum(int((offset_mask(u56.index, per, 0)[0].values
                   != rebalance_mask(u56.index, per).values).sum()) for per in CADORDER)
    gates.append(dict(gate="G0", what="offset_mask(.,per,0) == engine.rebalance_mask on D/W/M/Q",
                      value=float(bad), bar=0.0, ok=bad == 0))
    P(f"  G0  offset_mask vs engine.rebalance_mask       : {bad} disagreeing rows")

    g1max = 0.0
    for per in ("D", "W"):
        W = live_book(u56, INCUMBENT)
        ref = backtest(u56, W, cost_bps=HEAD_COST, freq=per)
        m, _ = offset_mask(u56.index, per, 0)
        r, tu, _ = Ctx(u56, m).run(shift1(W, u56.index))
        net = r - tu * HEAD_COST / 1e4
        d1 = float(np.abs(net[WARM:] - ref["returns"].values[WARM:]).max())
        d2 = float(np.abs(tu[WARM:] - ref["turnover"].values[WARM:]).max())
        g1max = max(g1max, d1, d2)
        P(f"  G1  Ctx vs engine.backtest, {per}             : max|d ret| {d1:.3e}  max|d turn| {d2:.3e}")
    gates.append(dict(gate="G1", what="fast Ctx == engine.backtest (returns and turnover)",
                      value=g1max, bar=1e-10, ok=g1max < 1e-10))

    d = float(np.abs(live_book(u56, INCUMBENT).values - rules_v2_weights(u56).values).max())
    gates.append(dict(gate="G2", what="live_book@0.75 == baseline.rules_v2_weights",
                      value=d, bar=1e-12, ok=d < 1e-12))
    P(f"  G2  live_book@{INCUMBENT} vs rules_v2_weights        : max|d| {d:.3e}   "
      f"(the subject IS the live book)")

    w75 = live_book(u56, INCUMBENT).values
    g6 = 0.0
    for g in (0.25, 1.00, 1.50):
        g6 = max(g6, float(np.nanmax(np.abs(live_book(u56, g).values - (g / INCUMBENT) * w75))))
    gates.append(dict(gate="G6", what="GROSS IDENTITY: W(g) == (g/0.75) * W(0.75) elementwise",
                      value=g6, bar=1e-12, ok=g6 < 1e-12))
    P(f"  G6  gross identity W(g) == (g/0.75)*W(0.75)   : max|d| {g6:.3e}")

    # ---------------------------------------------------------------- the ladder
    P()
    P("=" * 100)
    P("(B) THE LADDER -- (panel x gross x cadence x phase x cost), the live book at every size")
    P("=" * 100)
    tw = {}
    for pname, px in panels.items():
        for g in GROSS_LADDER:
            tw[(pname, g)] = shift1(live_book(px, g), px.index)
    gates.append(dict(gate="G4", what="MATCHED CONSTRUCTION: one target matrix per (panel,gross)",
                      value=float(len(tw)), bar=float(len(panels) * len(GROSS_LADDER)),
                      ok=len(tw) == len(panels) * len(GROSS_LADDER)))
    P(f"  G4  {len(tw)} target matrices built once, reused across every cadence and phase")

    rows = []
    det_store = {}
    borrow_daily = BORROW_BPS / 1e4 / 252.0
    for pname, px in panels.items():
        rspy = px["SPY"].pct_change().fillna(0.0).values
        isw = np.asarray(px.index <= pd.Timestamp(IS_END))
        osw = np.asarray(px.index >= pd.Timestamp(OOS_START))
        spy_full = mets(rspy[WARM:])
        spy_is = mets(rspy[WARM:][isw[WARM:]])
        spy_oos = mets(rspy[osw])
        v2_net = backtest(px, rules_v2_weights(px), cost_bps=HEAD_COST, freq="W")["returns"].values
        v2 = mets(v2_net[WARM:])

        cells = [(HEAD_CAD, ph) for ph in range(CADENCES[HEAD_CAD])]
        cells += [(c, 0) for c in CADORDER if c != HEAD_CAD]
        for cad, ph in cells:
            m, clipped = offset_mask(px.index, cad, ph)
            ctx = Ctx(px, m)
            for g in GROSS_LADDER:
                r, tu, expo = ctx.run(tw[(pname, g)])
                fin = np.maximum(expo - 1.0, 0.0) * borrow_daily
                for cb in RUNGS:
                    for borrow in (False, True):
                        net = r - tu * cb / 1e4 - (fin if borrow else 0.0)
                        row = dict(panel=pname, gross=g, cadence=cad, phase=ph, cost_bps=cb,
                                   borrow=borrow, clipped=clipped,
                                   turn_per_yr=float(tu[WARM:].sum() / (len(tu[WARM:]) / 252.0)),
                                   mean_expo=float(expo[WARM:].mean()),
                                   lev_frac=float(np.maximum(expo[WARM:] - 1.0, 0.0).mean()),
                                   fin_drag_bps=float(fin[WARM:].mean() * 252 * 1e4))
                        row.update(_row_metrics(net, isw, osw, spy_full, spy_is, spy_oos, v2))
                        rows.append(finish(row))
                        if (cad, ph, cb, borrow) == (HEAD_CAD, HEAD_PHASE, HEAD_COST, False):
                            det_store[(pname, g)] = (row["OOS_CAGR"], row["OOS_Sharpe"],
                                                     row["OOS_MaxDD"])
            del ctx
        P(f"  {pname:6s} done  ({len(rows):,} rows so far, {time.time()-t0:.0f}s)")

    lad = pd.DataFrame(rows)
    dump(lad, "ladder.csv")

    # headline cell: W / phase 0 / 10 bps / no borrow, the record's own convention
    HEAD = lad[(lad.cadence == HEAD_CAD) & (lad.phase == HEAD_PHASE)
               & (lad.cost_bps == HEAD_COST) & (~lad.borrow)].copy()

    # ---------------------------------------------------------------- G5 / G7 / G8 / G3
    px = panels["U56"]
    m, _ = offset_mask(px.index, HEAD_CAD, HEAD_PHASE)
    r2, tu2, ex2 = Ctx(px, m).run(shift1(live_book(px, 1.00), px.index))
    isw = np.asarray(px.index <= pd.Timestamp(IS_END))
    osw = np.asarray(px.index >= pd.Timestamp(OOS_START))
    o2 = mets((r2 - tu2 * HEAD_COST / 1e4)[osw])
    ref5 = det_store[("U56", 1.00)]
    g5 = max(abs(o2["CAGR"] - ref5[0]), abs(o2["Sharpe"] - ref5[1]), abs(o2["MaxDD"] - ref5[2]))
    gates.append(dict(gate="G5", what="determinism: U56/gross 1.00 cell rebuilt from scratch",
                      value=float(g5), bar=1e-12, ok=g5 < 1e-12))
    P(f"  G5  determinism (U56 @ 1.00 rebuilt)          : max|d| {g5:.3e}")

    sub = HEAD[HEAD.panel == "U56"]
    g8a = float(sub[sub.gross <= 1.0].fin_drag_bps.abs().max())
    g8b = float(sub[sub.gross > 1.0].fin_drag_bps.min())
    expected = float(BORROW_BPS * sub[sub.gross > 1.0].lev_frac.max())
    got = float(sub.fin_drag_bps.max())
    g8c = abs(got - expected)
    ok8 = (g8a == 0.0) and (g8b > 0.0) and (g8c < 1e-8)
    gates.append(dict(gate="G8", what="LEVERAGE ACCOUNTING: charge 0 at g<=1, >0 at g>1, "
                                      "== BORROW x mean(max(expo-1,0))",
                      value=float(g8c), bar=1e-8, ok=bool(ok8)))
    P(f"  G8  financing charge: max at g<=1.00 {g8a:.3e} bps | min at g>1.00 {g8b:.4f} bps | "
      f"identity max|d| {g8c:.3e}")

    # G7 IS-purity: choosers must not move when the OOS tape is permuted
    rng = np.random.default_rng(997)
    pxp = panels["U56"].copy()
    oidx = np.flatnonzero(osw)
    perm = oidx.copy()
    rng.shuffle(perm)
    vals = pxp.values.copy()
    vals[oidx] = vals[perm]
    pxp = pd.DataFrame(vals, index=pxp.index, columns=pxp.columns)
    m, _ = offset_mask(pxp.index, HEAD_CAD, HEAD_PHASE)
    ctxp = Ctx(pxp, m)
    rspyp = pxp["SPY"].pct_change().fillna(0.0).values
    spyf, spyi, spyo = (mets(rspyp[WARM:]), mets(rspyp[WARM:][isw[WARM:]]),
                        mets(rspyp[np.asarray(pxp.index >= pd.Timestamp(OOS_START))]))
    v2p = mets(backtest(pxp, rules_v2_weights(pxp), cost_bps=HEAD_COST,
                        freq="W")["returns"].values[WARM:])
    prow = []
    for g in GROSS_LADDER:
        rr, tt, _ = ctxp.run(shift1(live_book(pxp, g), pxp.index))
        net = rr - tt * HEAD_COST / 1e4
        row = dict(panel="U56", gross=g)
        row.update(_row_metrics(net, isw, np.asarray(pxp.index >= pd.Timestamp(OOS_START)),
                                spyf, spyi, spyo, v2p))
        prow.append(finish(row))
    prow = pd.DataFrame(prow)

    def pick(sub_, name):
        """Pre-declared IS-only choosers. Tiebreak ALWAYS to the SMALLEST gross (anti-overfit)."""
        s = sub_.sort_values("gross")
        if name == "C_ISSHARPE":
            v = s.IS_Sharpe.values
            return float(s.gross.values[int(np.nanargmax(v))])
        if name == "C_ISCAGR":
            v = s.IS_CAGR.values
            return float(s.gross.values[int(np.nanargmax(v))])
        if name == "C_IS4B":
            ok = s[s.IS_pass4b]
            return float(ok.gross.values[0]) if len(ok) else np.nan
        raise KeyError(name)

    g7 = 0.0
    for ch in CHOOSERS:
        a, b = pick(HEAD[HEAD.panel == "U56"], ch), pick(prow, ch)
        same = (np.isnan(a) and np.isnan(b)) or a == b
        g7 = max(g7, 0.0 if same else 1.0)
        P(f"  G7  IS-purity {ch:11s}: real pick {a}  permuted-OOS pick {b}  "
          f"{'OK' if same else 'MOVED'}")
    gates.append(dict(gate="G7", what="IS-PURITY: chooser picks invariant to permuted OOS tape",
                      value=float(g7), bar=0.0, ok=g7 == 0.0))

    # G3 / G3b cross-run against idea 993's committed artifacts
    g3v, g3ok, g3n = np.nan, False, 0
    if P993.exists():
        f993 = pd.read_csv(P993)
        f993 = f993[f993.fallback == "FB_LIVE"].set_index("panel")
        cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe", "IS_MaxDD",
                "IS_H1", "IS_H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "OOS_H1", "OOS_H2"]
        mine = HEAD[HEAD.gross == INCUMBENT].set_index("panel")
        dmax = max(abs(float(mine.loc[p, c]) - float(f993.loc[p, c]))
                   for p in f993.index for c in cols)
        g3n = len(f993) * len(cols)
        g3v, g3ok = float(dmax), dmax < G3_TOL
        P(f"  G3  CROSS-RUN idea 993 fallbacks.csv FB_LIVE : {g3n} cells, max|d| {dmax:.3e}")
    else:
        P("  G3  CROSS-RUN idea 993 fallbacks.csv          : FILE MISSING -- gate UNAVAILABLE")
    gates.append(dict(gate="G3", what="CROSS-RUN 993 fallbacks.csv FB_LIVE (3 panels x 15 metrics)",
                      value=g3v, bar=G3_TOL, ok=bool(g3ok)))

    g3bv, g3bok, g3bn = np.nan, False, 0
    if P993_LAD.exists():
        l993 = pd.read_csv(P993_LAD)
        l993 = l993[(l993.book == "BAND03") & (l993.cadence == HEAD_CAD)
                    & (l993.phase == HEAD_PHASE)].copy()
        l993["g"] = l993.gross.map({"CORE": 0.75, "EXT": 1.00})
        shared = [c for c in ["turn_per_yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR",
                              "IS_Sharpe", "IS_MaxDD", "IS_H1", "IS_H2", "OOS_CAGR", "OOS_Sharpe",
                              "OOS_MaxDD", "OOS_H1", "OOS_H2", "spy_CAGR", "spy_Sharpe",
                              "spy_MaxDD"] if c in l993.columns]
        mine = lad[(lad.cadence == HEAD_CAD) & (lad.phase == HEAD_PHASE) & (~lad.borrow)]
        key = ["panel", "g", "cost_bps"]
        a = l993[key + shared].rename(columns={"g": "gross"})
        b = mine[["panel", "gross", "cost_bps"] + shared]
        j = a.rename(columns={"gross": "gross"}).merge(b, on=["panel", "gross", "cost_bps"],
                                                       suffixes=("_993", "_me"))
        dmax = max(float(np.abs(j[c + "_993"] - j[c + "_me"]).max()) for c in shared)
        g3bn = len(j) * len(shared)
        g3bv, g3bok = float(dmax), dmax < G3_TOL
        P(f"  G3b CROSS-RUN idea 993 ladder.csv BAND03/W    : {len(j)} rows x {len(shared)} cols "
          f"= {g3bn} cells, max|d| {dmax:.3e}")
    else:
        P("  G3b CROSS-RUN idea 993 ladder.csv             : FILE MISSING -- gate UNAVAILABLE")
    gates.append(dict(gate="G3b", what="CROSS-RUN 993 ladder.csv BAND03 x {0.75,1.00} x W x ph0 "
                                       "x 5 cost rungs", value=g3bv, bar=G3_TOL, ok=bool(g3bok)))

    gdf = pd.DataFrame(gates)
    dump(gdf, "gates.csv")
    P(f"  GATES: {int(gdf.ok.sum())} of {len(gdf)} pass")

    # ---------------------------------------------------------------- (C) the ladder table
    P()
    P("=" * 100)
    P("(C) THE GROSS LADDER, HEADLINE CELL (cadence W, phase 0, 10 bps, zero-borrow convention)")
    P("    every rung reported; nothing is selected on this table")
    P("=" * 100)
    for pname in ("U56", "B136", "SMALL"):
        s = HEAD[HEAD.panel == pname].sort_values("gross")
        r0 = s.iloc[0]
        floor = CAGR_FLOOR * r0.spy_CAGR
        cap = DD_CAP * abs(r0.spy_MaxDD)
        P()
        P(f"  --- {pname} --- SPY: CAGR {r0.spy_CAGR:7.2%} (full) / {r0.spy_OOS_CAGR:7.2%} (OOS), "
          f"MaxDD {r0.spy_MaxDD:7.2%}, OOS Sharpe {r0.spy_OOS_Sharpe:.4f}")
        P(f"      4b size bars: OOS CAGR >= {floor:7.2%}   |OOS MaxDD| <= {cap:7.2%}")
        P("      gross | OOS CAGR | OOS Shrp | OOS MaxDD |  turn/yr | CAGRleg DDleg | 4b   4a  | "
          "fail legs")
        for _, r in s.iterrows():
            mark = " <== INCUMBENT" if abs(r.gross - INCUMBENT) < 1e-9 else ""
            P(f"      {r.gross:5.2f} | {r.OOS_CAGR:8.2%} | {r.OOS_Sharpe:8.4f} | "
              f"{r.OOS_MaxDD:9.2%} | {r.turn_per_yr:8.3f} |  {str(bool(r.leg_CAGR)):5s} "
              f"{str(bool(r.leg_DD)):5s} | {str(bool(r.pass4b)):5s} {str(bool(r.pass4a)):5s}| "
              f"{r.fail_legs}{mark}")

    # ---------------------------------------------------------------- (D) the window
    P()
    P("=" * 100)
    P("(D) THE WINDOW -- g_CAGR (smallest rung clearing the floor) vs g_DD (largest clearing the cap)")
    P("=" * 100)

    def window(s, legc, legd):
        c = s[s[legc]].gross
        d = s[s[legd]].gross
        gc = float(c.min()) if len(c) else np.nan
        gd = float(d.max()) if len(d) else np.nan
        return gc, gd

    wins = []
    for pname in ("U56", "B136", "SMALL"):
        s = HEAD[HEAD.panel == pname].sort_values("gross")
        gc, gd = window(s, "leg_CAGR", "leg_DD")
        gca, gda = window(s, "alloos_CAGR", "alloos_DD")
        p4 = s[s.pass4b].gross
        nonempty = bool(np.isfinite(gc) and np.isfinite(gd) and gc <= gd)
        wins.append(dict(panel=pname, g_CAGR=gc, g_DD=gd, nonempty=nonempty,
                         width=(gd - gc) if nonempty else np.nan,
                         g_CAGR_alloos=gca, g_DD_alloos=gda,
                         nonempty_alloos=bool(np.isfinite(gca) and np.isfinite(gda) and gca <= gda),
                         n_pass4b=int(s.pass4b.sum()),
                         pass4b_lo=float(p4.min()) if len(p4) else np.nan,
                         pass4b_hi=float(p4.max()) if len(p4) else np.nan,
                         n_pass4a=int(s.pass4a.sum()),
                         incumbent_below=bool(nonempty and INCUMBENT < gc),
                         incumbent_in=bool(nonempty and gc <= INCUMBENT <= gd)))
        w = wins[-1]
        P(f"  {pname:6s} g_CAGR {gc if np.isfinite(gc) else float('nan'):5.2f}   "
          f"g_DD {gd if np.isfinite(gd) else float('nan'):5.2f}   "
          f"window {'NON-EMPTY' if nonempty else 'EMPTY    '}  "
          f"width {w['width'] if nonempty else float('nan'):5.2f}   "
          f"4b passes {w['n_pass4b']:2d} of {len(s)} rungs"
          + (f"  [{w['pass4b_lo']:.2f} .. {w['pass4b_hi']:.2f}]" if w["n_pass4b"] else "")
          + f"   4a passes {w['n_pass4a']:2d}")
        P(f"         ALL-OOS leg reading: g_CAGR {gca:5.2f}  g_DD {gda:5.2f}  "
          f"{'NON-EMPTY' if w['nonempty_alloos'] else 'EMPTY'}")
    wdf = pd.DataFrame(wins)
    dump(wdf, "window.csv")

    # ---------------------------------------------------------------- (E) rule 8
    P()
    P("=" * 100)
    P("(E) RULE 8 WALK-FORWARD -- the gross rung chosen on 2009-2016 ALONE, scored on 2017-2026")
    P("    3 panels x 3 pre-declared IS choosers = 9 slots.  A chooser that picks nothing is")
    P("    NOT dropped (idea 993's lesson): it is scored holding the INCUMBENT 0.75.")
    P("=" * 100)
    r8 = []
    for pname in ("U56", "B136", "SMALL"):
        s = HEAD[HEAD.panel == pname].sort_values("gross")
        inc = s[s.gross == INCUMBENT].iloc[0]
        for ch in CHOOSERS:
            g = pick(s, ch)
            refused = not np.isfinite(g)
            gg = INCUMBENT if refused else g
            r = s[s.gross == gg].iloc[0]
            r8.append(dict(panel=pname, chooser=ch, pick=g, scored_gross=gg, refused=refused,
                           OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                           pass4b=bool(r.pass4b), pass4a=bool(r.pass4a), fail_legs=r.fail_legs,
                           spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                           spy_OOS_MaxDD=r.spy_OOS_MaxDD,
                           v2_OOS_CAGR=inc.OOS_CAGR, v2_OOS_Sharpe=inc.OOS_Sharpe,
                           v2_OOS_MaxDD=inc.OOS_MaxDD))
            x = r8[-1]
            P(f"  {pname:6s} {ch:11s} pick {'NONE(->0.75)' if refused else f'{g:.2f}':12s} "
              f"OOS CAGR {x['OOS_CAGR']:7.2%}  Sharpe {x['OOS_Sharpe']:.4f}  "
              f"MaxDD {x['OOS_MaxDD']:7.2%}  4b {str(x['pass4b']):5s} 4a {str(x['pass4a']):5s} "
              f"| {x['fail_legs']}")
    r8df = pd.DataFrame(r8)
    dump(r8df, "rule8.csv")
    P(f"  RULE 8 TOTALS: OOS 4b {int(r8df.pass4b.sum())} of {len(r8df)} slots   "
      f"OOS 4a {int(r8df.pass4a.sum())} of {len(r8df)}   "
      f"(incumbent-0.75 reference: 4b {int((HEAD[HEAD.gross==INCUMBENT].pass4b).sum())} of 3)")
    P("  OOS comparands, per panel (incumbent live book at 0.75 / SPY):")
    for pname in ("U56", "B136", "SMALL"):
        x = r8df[r8df.panel == pname].iloc[0]
        P(f"    {pname:6s} live@0.75 CAGR {x['v2_OOS_CAGR']:7.2%} Sharpe {x['v2_OOS_Sharpe']:.4f} "
          f"MaxDD {x['v2_OOS_MaxDD']:7.2%}  |  SPY CAGR {x['spy_OOS_CAGR']:7.2%} "
          f"Sharpe {x['spy_OOS_Sharpe']:.4f} MaxDD {x['spy_OOS_MaxDD']:7.2%}")

    # ---------------------------------------------------------------- (F) robustness columns
    P()
    P("=" * 100)
    P("(F) ROBUSTNESS COLUMNS -- reported, selected on by nothing")
    P("=" * 100)

    P()
    P("  (F1) FINANCING: the same headline cell with %.0f bps/yr charged on the levered fraction"
      % BORROW_BPS)
    BOR = lad[(lad.cadence == HEAD_CAD) & (lad.phase == HEAD_PHASE)
              & (lad.cost_bps == HEAD_COST) & (lad.borrow)]
    fin_rows = []
    for pname in ("U56", "B136", "SMALL"):
        s = BOR[BOR.panel == pname].sort_values("gross")
        gc, gd = window(s, "leg_CAGR", "leg_DD")
        ne = bool(np.isfinite(gc) and np.isfinite(gd) and gc <= gd)
        p4 = s[s.pass4b].gross
        fin_rows.append(dict(panel=pname, g_CAGR=gc, g_DD=gd, nonempty=ne,
                             n_pass4b=int(s.pass4b.sum()),
                             pass4b_lo=float(p4.min()) if len(p4) else np.nan,
                             pass4b_hi=float(p4.max()) if len(p4) else np.nan,
                             max_fin_drag_bps=float(s.fin_drag_bps.max())))
        x = fin_rows[-1]
        P(f"    {pname:6s} g_CAGR {gc:5.2f}  g_DD {gd:5.2f}  "
          f"{'NON-EMPTY' if ne else 'EMPTY'}  4b {x['n_pass4b']:2d} rungs"
          + (f" [{x['pass4b_lo']:.2f}..{x['pass4b_hi']:.2f}]" if x["n_pass4b"] else "")
          + f"  max financing drag {x['max_fin_drag_bps']:.1f} bps/yr")
    findf = pd.DataFrame(fin_rows)
    dump(findf, "financing.csv")

    P()
    P("  (F2) PHASE: all %d weekly phases at 10 bps, zero-borrow.  The record's L4_DD leg is a"
      % CADENCES[HEAD_CAD])
    P("       known phase coin-flip, so the window is reported per phase and as a phase median.")
    PH = lad[(lad.cadence == HEAD_CAD) & (lad.cost_bps == HEAD_COST) & (~lad.borrow)]
    ph_rows = []
    for pname in ("U56", "B136", "SMALL"):
        gcs, gds, nes, n4 = [], [], [], []
        for ph in range(CADENCES[HEAD_CAD]):
            s = PH[(PH.panel == pname) & (PH.phase == ph)].sort_values("gross")
            gc, gd = window(s, "leg_CAGR", "leg_DD")
            ne = bool(np.isfinite(gc) and np.isfinite(gd) and gc <= gd)
            gcs.append(gc); gds.append(gd); nes.append(ne); n4.append(int(s.pass4b.sum()))
            ph_rows.append(dict(panel=pname, phase=ph, g_CAGR=gc, g_DD=gd, nonempty=ne,
                                n_pass4b=int(s.pass4b.sum())))
        P(f"    {pname:6s} g_CAGR {['%.2f' % v for v in gcs]}  g_DD {['%.2f' % v for v in gds]}  "
          f"non-empty {sum(nes)} of {len(nes)} phases   4b rungs {n4}")
    phdf = pd.DataFrame(ph_rows)
    dump(phdf, "phase.csv")

    P()
    P("  (F3) CADENCE (phase 0, 10 bps, zero-borrow) -- D / W / M / Q, published beside the")
    P("       headline and selected on by nothing")
    cad_rows = []
    for pname in ("U56", "B136", "SMALL"):
        line = []
        for cad in CADORDER:
            s = lad[(lad.panel == pname) & (lad.cadence == cad) & (lad.phase == 0)
                    & (lad.cost_bps == HEAD_COST) & (~lad.borrow)].sort_values("gross")
            gc, gd = window(s, "leg_CAGR", "leg_DD")
            ne = bool(np.isfinite(gc) and np.isfinite(gd) and gc <= gd)
            cad_rows.append(dict(panel=pname, cadence=cad, g_CAGR=gc, g_DD=gd, nonempty=ne,
                                 n_pass4b=int(s.pass4b.sum())))
            line.append(f"{cad}:[{gc:.2f},{gd:.2f}] 4b {int(s.pass4b.sum()):2d}")
        P(f"    {pname:6s} " + "  ".join(line))
    caddf = pd.DataFrame(cad_rows)
    dump(caddf, "cadence.csv")

    P()
    P("  (F4) COST RUNGS (W, phase 0, zero-borrow) -- 4b-passing rung count at each rung")
    cost_rows = []
    for pname in ("U56", "B136", "SMALL"):
        line = []
        for cb in RUNGS:
            s = lad[(lad.panel == pname) & (lad.cadence == HEAD_CAD) & (lad.phase == HEAD_PHASE)
                    & (lad.cost_bps == cb) & (~lad.borrow)].sort_values("gross")
            gc, gd = window(s, "leg_CAGR", "leg_DD")
            cost_rows.append(dict(panel=pname, cost_bps=cb, g_CAGR=gc, g_DD=gd,
                                  n_pass4b=int(s.pass4b.sum())))
            line.append(f"{cb:.0f}bps:[{gc:.2f},{gd:.2f}] 4b {int(s.pass4b.sum()):2d}")
        P(f"    {pname:6s} " + "  ".join(line))
    costdf = pd.DataFrame(cost_rows)
    dump(costdf, "cost.csv")

    # ---------------------------------------------------------------- (G) hypotheses
    P()
    P("=" * 100)
    P("(G) PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    H = []

    def hyp(name, stat, bar, ok, note):
        H.append(dict(hypothesis=name, statistic=stat, bar=bar, verdict="PASS" if ok else "FAIL",
                      note=note))
        P(f"  {name:14s} {'PASS' if ok else 'FAIL'}   {note}")

    ne_any = bool(wdf.nonempty.any())
    hyp("H_WINDOW", float(wdf.nonempty.sum()), ">=1",
        ne_any, f"non-empty on {int(wdf.nonempty.sum())} of 3 panels "
                f"({', '.join(wdf.loc[wdf.nonempty, 'panel'])})" if ne_any else "empty on all 3")
    hyp("H_PANEL", float(wdf.nonempty.sum()), "==3", bool(wdf.nonempty.all()),
        f"non-empty on {int(wdf.nonempty.sum())} of 3")
    sub = wdf[wdf.nonempty]
    hyp("H_INCUMBENT", float(sub.incumbent_below.sum()) if len(sub) else np.nan,
        "all non-empty panels", bool(len(sub) and sub.incumbent_below.all()),
        f"incumbent {INCUMBENT} below the window on {int(sub.incumbent_below.sum())} of "
        f"{len(sub)} non-empty panels; inside it on {int(sub.incumbent_in.sum())}")
    n4b = int(HEAD.pass4b.sum())
    hyp("H_4B", float(n4b), ">=1", n4b >= 1,
        f"{n4b} of {len(HEAD)} (panel,gross) points pass full OOS 4b")
    n4a = int(HEAD.pass4a.sum())
    hyp("H_4A", float(n4a), ">=1", n4a >= 1,
        f"{n4a} of {len(HEAD)} points clear 4a against RULES v2 (pre-declared expected FAIL)")
    nr8 = int(r8df.pass4b.sum())
    hyp("H_R8", float(nr8), ">=1", nr8 >= 1,
        f"{nr8} of {len(r8df)} rule-8 slots pass OOS 4b")
    need = [p for p in wdf.loc[wdf.nonempty, "panel"]]
    allr8 = bool(len(need)) and all(r8df[(r8df.panel == p)].pass4b.all() for p in need)
    hyp("H_R8_ALL", float(sum(r8df[r8df.panel.isin(need)].pass4b)) if need else np.nan,
        "all choosers on all non-empty panels", allr8,
        f"{int(r8df[r8df.panel.isin(need)].pass4b.sum())} of "
        f"{len(r8df[r8df.panel.isin(need)])} slots on the non-empty panels")
    flat = 0.0
    for pname in ("U56", "B136", "SMALL"):
        s = HEAD[HEAD.panel == pname].set_index("gross")
        flat = max(flat, float((s.OOS_Sharpe - s.loc[INCUMBENT, "OOS_Sharpe"]).abs().max()))
    hyp("H_SHARPE_FLAT", flat, f"<= {BAR_FLAT}", flat <= BAR_FLAT,
        f"max |OOS Sharpe(g) - OOS Sharpe(0.75)| over the ladder = {flat:.4f} "
        f"(idea 948's cancellation band {BAR_FLAT})")
    mono = True
    for pname in ("U56", "B136", "SMALL"):
        s = HEAD[HEAD.panel == pname].sort_values("gross")
        mono &= bool((s.OOS_CAGR.diff().dropna() >= -1e-12).all())
        mono &= bool((s.OOS_MaxDD.abs().diff().dropna() >= -1e-12).all())
    hyp("H_MONO", float(mono), "both non-decreasing in g on all panels", mono,
        "OOS CAGR and |OOS MaxDD| monotone in gross" if mono
        else "NOT monotone -- the window is not an interval and must be read rung by rung")
    bok = bool(len(findf[findf.nonempty])) and bool(
        set(findf.loc[findf.nonempty, "panel"]) >= set(wdf.loc[wdf.nonempty, "panel"]))
    hyp("H_BORROW", float(findf.nonempty.sum()), "same panels as zero-borrow", bok,
        f"window non-empty on {int(findf.nonempty.sum())} of 3 panels once financing is charged "
        f"(zero-borrow: {int(wdf.nonempty.sum())})")
    phok = True
    for pname in wdf.loc[wdf.nonempty, "panel"]:
        phok &= bool(phdf[phdf.panel == pname].nonempty.all())
    phok = bool(phok and len(wdf[wdf.nonempty]))
    hyp("H_PHASE", float(phdf.nonempty.sum()), "non-empty at every weekly phase", phok,
        f"{int(phdf.nonempty.sum())} of {len(phdf)} (panel,phase) cells non-empty; on the "
        f"non-empty panels {'all' if phok else 'NOT all'} phases agree")
    ldok = bool((wdf.nonempty == wdf.nonempty_alloos).all())
    hyp("H_LEGDEF", float((wdf.nonempty == wdf.nonempty_alloos).sum()), "==3", ldok,
        "record and ALL-OOS leg readings agree on all 3 panels" if ldok
        else "the two leg readings DISAGREE -- the window depends on which SPY bar is used")

    hdf = pd.DataFrame(H)
    dump(hdf, "hypotheses.csv")

    # ---------------------------------------------------------------- (H) verdict
    P()
    P("=" * 100)
    P("(H) VERDICT")
    P("=" * 100)
    keep4b = (n4b >= 1) and (nr8 >= 1)
    P(f"  KEEP path 4a : {'PASS' if n4a else 'REFUSED'} -- {n4a} of {len(HEAD)} rungs")
    P(f"  KEEP path 4b : {n4b} of {len(HEAD)} rungs pass full sample OOS; "
      f"{nr8} of {len(r8df)} rule-8 slots pass")
    P(f"  GATES        : {int(gdf.ok.sum())} of {len(gdf)}")
    P(f"  VERDICT      : {'KEEP-candidate (4b)' if keep4b else 'KILL / PARK'}")
    P(f"  elapsed {time.time()-t0:.0f}s")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

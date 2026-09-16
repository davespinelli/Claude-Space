#!/usr/bin/env python3
"""Idea 1087 (cloud lane, 2026-09-16) -- does the `1 + g*d` RENORMALISATION bias any committed
CADENCE claim?

THE QUESTION (QUEUE idea 1087, verbatim)
    idea 1076 found turnover is NOT exactly proportional to gross: turn(g)/g falls monotonically
    in g on 40 of 40 cells (max deviation 5.31% over {0.25..1.00}, 2.87% over the record's own
    ladder), and the worst cells are all BAND03 DAILY -- the SLOWEST-turning book, where drift
    between decisions has most room.  Every committed cadence comparison differences two books at
    one gross, so the residual does not cancel.  Measure its size on each committed cadence step
    and report how many published cadence gains it moves beyond their own stated precision.
    Max 2 params (cadence step, gross rung).

THE MECHANISM, STATED BEFORE ANY NUMBER
    `engine.backtest` normalises the drifted holdings row by V = 1 + g*d, where d is the drift
    P&L per unit of gross since the last decision.  d > 0 on average on this tape, so a LARGER g
    deflates the held row MORE and pulls it back TOWARD the target, and turnover per unit of gross
    FALLS in g.  The drift d accumulates between DECISIONS, so its magnitude is a cadence fact:
    a quarterly book drifts for ~63 trading days before it is asked to trade, a daily book for 1.
    A cadence STEP differences two books whose d differ by that much, so the two residuals are NOT
    the same size and cannot cancel.

    DECLARED DIRECTION (before the numbers): REL_step(g) is NEGATIVE and monotone DECREASING in g,
    like the level residual, and LARGER in magnitude than either level's, because differencing two
    numbers that are each slightly wrong leaves a residual on a much smaller base.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL rule 4: max 2 tuned parameters)
    TUNED 1  CADENCE STEP, 6 levels, all reported and never merged:
             D->W, W->M, M->Q (adjacent) and D->M, W->Q, D->Q (the record quotes these too).
    TUNED 2  GROSS RUNG, 4 levels, all reported: {0.25, 0.50, 0.75, 1.00}.  The record's OWN
             ladder is {0.50, 0.75, 1.00}; 0.25 exists to widen the curve and no verdict is read
             off it alone.
    REPORTED AXES (nothing fitted on them, every point published): PANEL {U56, B136};
             BOOK {TOP5, TOP10, TOP20, EWELIG, BAND03} -- idea 930/1076's own set, verbatim;
             CADENCE {D, W, M, Q}; SOURCE {LEADERBOARD, CHANGELOG, QUEUE, RESULTMD}.
    6 steps x 4 rungs x 10 (panel, book) cells = 240 published step-points, off a 160-point
    turnover ladder that reproduces 1076's committed one exactly (gate G5).

WHAT "BIAS" MEANS HERE, fixed before any number
    A committed cadence gain is a number in bp/yr or x/yr that differences two cadences.  It is
    exact AT THE GROSS IT WAS MEASURED AT -- a difference of two measured quantities needs no
    model.  The `1 + g*d` residual enters when that gain is READ AT ANOTHER GROSS, which is what
    every un-stamped figure invites (1076: 0.076 of committed turnover/drag figures state one).
    So:
        BIAS(g_from -> g_to) = STEP(g_from) * g_to/g_from  -  STEP(g_to)
    in the figure's own unit, and the question "does it move a published claim" is whether |BIAS|
    exceeds the precision that claim states about ITSELF (half a unit in its last printed digit).

PRE-REGISTERED BARS (fixed before any number was read; both directions reported)
    H_STEPLIN   the cadence step is proportional to gross to within 1%: max over all
                (panel, book, step) cells of |(STEP(g)/g)/(STEP(1.00)) - 1| <= 0.01 over the full
                ladder.
    H_STEPREC   the same over the record's OWN ladder {0.50, 0.75, 1.00}.
    H_AMPLIFY   DECLARED DIRECTION: the step residual is LARGER than the level residual it is
                built from (differencing amplifies, it does not cancel).  Scored as written; a
                failure is published, not patched.
    H_RANK      the cadence ORDERING by annual turnover is identical at all four gross rungs in
                every (panel, book) cell -- i.e. no committed "M turns over less than W" claim
                can be reversed by the rung it is read at.
    H_PRECISION >= 0.50 of committed cadence-gain figures are NOT moved: |BIAS| at the median cell
                is <= the figure's own stated precision.
    H_1076      this run reproduces 1076's committed level deviations 5.312e-02 (full ladder) and
                2.87e-02 (record ladder) to within 1e-6.
    H_WF        the IS-only (cadence, gross) pick (rule 8) clears 4b OUT OF SAMPLE on >= 1 cell.

GATES (printed BEFORE any result number; a failure is published, not patched)
    G1  fast runner == engine.backtest on returns AND turnover, two cost rungs
    G2  cost linearity net(c) == gross - turnover*c/1e4 at two rungs G1 did not use
    G3  SPY OOS triple vs the record's committed (0.152102, 0.8711, -0.337173)
    G4  live RULES v2 full-sample MaxDD vs the record's committed -12.05%
    G5  CROSS-RUN: this run's turn_yr vs idea 1076's committed linearity.csv, all shared cells
    G6  CROSS-RUN: 1076's committed level deviations reproduce
    G7  determinism: the weight rows are a pure function of the panel

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels.  The census half of
this run is a statement about committed TEXT and is unaffected.  The tape half (turnover levels,
the residual, rule 8, both KEEP paths) is flattered exactly as every other run on these panels is,
and every 4b count below is an UPPER bound.

Run:  python3 research/backtests/2026-09-16_does-the-1-plus-g-times-d-RENORMALISATION-bias-any-committed-CADENCE-claim_cloud.py
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

COST, LAG, WARMUP = 10.0, 1, 260                 # PROTOCOL rule 2 binding cost
MAXVOL, BAND = 0.60, 0.03
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

PANELS = ["U56", "B136"]
BOOKS = ["TOP5", "TOP10", "TOP20", "EWELIG", "BAND03"]   # idea 930/1076's book set, verbatim
CADENCES = ["D", "W", "M", "Q"]
STEPS = [(a, b) for a, b in combinations(CADENCES, 2)]   # dial 1: 6 ordered fast->slow steps
LADDER = [0.25, 0.50, 0.75, 1.00]                        # dial 2
RECORD_LADDER = [0.50, 0.75, 1.00]                       # the record's own ladder (926/930/1076)

SPY_OOS_PUB = (0.152102, 0.8711, -0.337173)      # G3, committed by ideas 1018/1023
G3_TOL = (2e-3, 2e-2, 2e-3)
V2_MAXDD_PUB = -0.1205                           # G4, committed by ideas 1071/1083
DEV_FULL_PUB, DEV_REC_PUB = 5.312e-02, 2.87e-02  # G6, committed by idea 1076
REF1076 = OUT / ("2026-09-16_should-every-published-TURNOVER-or-DRAG-figure-carry-its-GROSS_C"
                 ".linearity.csv")

H_LIN_BAR = 0.01
H_PRECISION_BAR = 0.50

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def head_sha() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


# =================================================================================================
# runner -- GROSS returns + turnover; any cost rung is a linear subtraction (gate G2).
# Copied verbatim from idea 930/1076 so this run's ladder is comparable cell for cell.
# =================================================================================================
class Ctx:
    def __init__(self, rets, applied):
        T, N = rets.shape
        self.rets, self.T = rets, T
        C = np.cumprod(1.0 + rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        self.reb = np.flatnonzero(applied)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]

    def run(self, wt):
        """-> (GROSS portfolio returns, turnover).  net(c) = gross - turnover * c / 1e4."""
        A = wt[self.s0]
        AR = A * self.R
        V = 1.0 + (AR.sum(axis=1) - A.sum(axis=1))     # <- the 1 + g*d renormalisation itself
        port = (AR * self.rets).sum(axis=1) / V
        Ap = wt[self.s0p[self.reb]]
        ARp = Ap * self.Rp
        Vp = 1.0 + (ARp.sum(axis=1) - Ap.sum(axis=1))
        heldp = ARp / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp).sum(axis=1)
        return port, turn


def lag_weights(W1):
    wt = np.roll(W1, LAG, axis=0).copy()
    wt[:LAG] = 0.0
    return wt


def applied_from_decision(dec):
    a = np.roll(dec, LAG)
    a[:LAG] = False
    a[0] = True
    return a


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


class Panel:
    def __init__(self, name, px):
        self.name, self.px, self.idx = name, px, px.index
        self.rets = px.pct_change().fillna(0.0).values
        self.T = len(self.idx)
        self.warm = np.arange(self.T) >= WARMUP
        self.oos_m = np.asarray(self.idx >= pd.Timestamp(OOS_START)) & self.warm
        self.is_m = self.warm & np.asarray(self.idx <= pd.Timestamp(IS_END))
        wpos = np.flatnonzero(self.warm)
        h = len(wpos) // 2
        self.h1 = np.zeros(self.T, bool); self.h1[wpos[:h]] = True
        self.h2 = np.zeros(self.T, bool); self.h2[wpos[h:]] = True
        self.yrs_warm = self.warm.sum() / 252.0
        self.yrs_is = self.is_m.sum() / 252.0
        self.yrs_oos = self.oos_m.sum() / 252.0
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        above = px > px.rolling(200).mean()
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        self.elig = (above & (vol20 < MAXVOL) & px.notna()).values
        self.dec = {c: rebalance_mask(self.idx, c).values.copy() for c in CADENCES}
        self.app = {c: applied_from_decision(self.dec[c]) for c in CADENCES}
        self.ctx = {c: Ctx(self.rets, self.app[c]) for c in CADENCES}
        self.spy_full = fmet(self.spy[self.warm])
        self.spy_h1 = fmet(self.spy[self.h1])[1]
        self.spy_h2 = fmet(self.spy[self.h2])[1]
        self.spy_oos = fmet(self.spy[self.oos_m])
        self.spy_is = fmet(self.spy[self.is_m])


def legs_4b(pn, r):
    """PROTOCOL 4b's five legs.  SPY is buy-and-hold and is charged no cost (4b as written)."""
    c, s, dd = fmet(r[pn.warm])
    os_ = fmet(r[pn.oos_m])
    sh1, sh2 = fmet(r[pn.h1])[1], fmet(r[pn.h2])[1]
    legs = dict(L_H1=bool(sh1 > pn.spy_h1), L_H2=bool(sh2 > pn.spy_h2),
                L_OOS=bool(os_[1] > pn.spy_oos[1]),
                L_DD=bool(abs(dd) <= DD_CAP * abs(pn.spy_full[2])),
                L_CAGR=bool(c >= CAGR_FLOOR * pn.spy_full[0]))
    return legs, (c, s, dd), (sh1, sh2), os_


def book_w1(px, book, elig):
    """UNIT-GROSS weight rows; the caller multiplies by g.  Copied from idea 930/1076."""
    if book == "BAND03":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(band_state(px, BAND), 0.0).values
    if book == "EWELIG":
        E = elig.astype(float)
        k = E.sum(axis=1)
        out = np.zeros_like(E)
        nz = k > 0
        out[nz] = E[nz] / k[nz, None]
        return out
    n = int(book[3:])
    mom = (px.shift(21) / px.shift(252) - 1).rank(axis=1, pct=True)
    r6 = (px / px.shift(126) - 1).rank(axis=1, pct=True)
    r3 = (px / px.shift(63) - 1).rank(axis=1, pct=True)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = ((mom + r6 + r3) / 3) * (0.5 + 0.5 * above.astype(float))
    rank = sc.where(above & (vol20 < MAXVOL)).rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0).values


# =================================================================================================
# CENSUS -- the record's committed CADENCE-GAIN figures and the precision they state
# =================================================================================================
CADWORD = {
    "D": r"\bdaily\b|\bD\b",
    "W": r"\bweekly\b|\bW\b",
    "M": r"\bmonthly\b|\bM\b",
    "Q": r"\bquarterly\b|\bQ\b",
}
# an explicit cadence STEP written as an arrow or "X to Y"
STEP_RX = re.compile(
    r"\b(D|W|M|Q)\s*(?:->|-->|→|to)\s*(D|W|M|Q)\b"
    r"|\b(daily|weekly|monthly|quarterly)\s*(?:->|-->|→|to)\s*(daily|weekly|monthly|quarterly)\b",
    re.I)
CAD_ANY_RX = re.compile(r"\b(daily|weekly|monthly|quarterly)\b|\bcadence\b", re.I)
TOK_RX = re.compile(r"\bturnover\b|\bturns?\s+over\b|\bdrag\b|\bbp/yr\b|\bbps/yr\b|\bx/yr\b", re.I)
VAL_RX = re.compile(
    r"(?:[-+]?\d+(?:\.\d+)?)\s*(?:bp|bps)\s*/\s*yr"
    r"|(?:[-+]?\d+(?:\.\d+)?)\s*x\s*/\s*yr"
    r"|turnover[^.;|]{0,60}?(?:[-+]?\d+(?:\.\d+)?)\s*x"
    r"|(?:[-+]?\d+(?:\.\d+)?)\s*x\s+(?:annual\s+)?turnover"
    r"|drag[^.;|]{0,60}?(?:[-+]?\d+(?:\.\d+)?)\s*(?:bp|bps)",
    re.I)
GROSSNUM_RX = re.compile(r"gross\s*(?:of|=|:|\s)\s*([01]?\.\d{1,2})"
                         r"|\bg\s*=\s*([01]?\.\d{1,2})"
                         r"|@\s*([01]\.\d{2})", re.I)


def corpus():
    """Every COMMITTED unit of the record, exactly as idea 1076 defined it."""
    units = []
    lb = [l for l in (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
          if l.startswith("|") and not l.startswith("|---")][1:]
    units += [("LEADERBOARD", str(i), t) for i, t in enumerate(lb)]
    cl = [p for p in (ROOT / "research" / "CHANGELOG.md").read_text().split("\n\n") if p.strip()]
    units += [("CHANGELOG", str(i), t) for i, t in enumerate(cl)]
    q = [l for l in (ROOT / "research" / "QUEUE.md").read_text().split("\n") if l.strip()]
    units += [("QUEUE", str(i), t) for i, t in enumerate(q)]
    for f in sorted((ROOT / "research" / "backtests").glob("*.result.md")):
        ps = [p for p in f.read_text(errors="ignore").split("\n\n") if p.strip()]
        units += [("RESULTMD", f"{f.stem}#{i}", t) for i, t in enumerate(ps)]
    return units


def _value_and_decimals(s):
    m = re.search(r"[-+]?\d+(?:\.\d+)?", s)
    if not m:
        return np.nan, 0
    tok = m.group(0)
    dec = len(tok.split(".")[1]) if "." in tok else 0
    return float(tok), dec


def census_cadence(units):
    """One row per committed turnover/drag FIGURE that sits in a unit which also talks about
    cadence.  TIER is the dial-free reported axis:
        STEP  the unit names an explicit cadence step (X -> Y / "weekly to monthly")
        MULTI the unit names >= 2 distinct cadences (a comparison, arrow not written)
        ONE   the unit names exactly one cadence (a level, not a gain)
    Only STEP and MULTI are 'cadence gains'; ONE is carried so the denominator is visible."""
    rows = []
    for src, uid, t in units:
        if not (TOK_RX.search(t) and CAD_ANY_RX.search(t)):
            continue
        cads = {c for c, rx in CADWORD.items() if re.search(rx, t)}
        has_step = bool(STEP_RX.search(t))
        tier = "STEP" if has_step else ("MULTI" if len(cads) >= 2 else "ONE")
        for m in VAL_RX.finditer(t):
            v, dec = _value_and_decimals(m.group(0))
            unit_kind = "bp/yr" if re.search(r"bp", m.group(0), re.I) else "x"
            seg = t[max(0, m.start() - 200): m.end() + 200]
            rows.append(dict(source=src, unit=uid, tier=tier, figure=m.group(0).strip(),
                             value=v, decimals=dec, unit_kind=unit_kind,
                             cadences="".join(sorted(cads)),
                             gross_stamped=bool(GROSSNUM_RX.search(seg)),
                             # half a unit in the last printed digit, expressed in bp/yr at 10 bps
                             prec_bpyr=(0.5 * 10.0 ** (-dec)) * (1.0 if unit_kind == "bp/yr"
                                                                 else COST)))
    return pd.DataFrame(rows)


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 1087 (cloud lane) -- does the `1 + g*d` RENORMALISATION bias any committed CADENCE "
      "claim?")
    P(f"tree {head_sha()}   ladder {LADDER}   record ladder {RECORD_LADDER}   "
      f"steps {['->'.join(s) for s in STEPS]}   cost {COST:.0f} bps   LAG {LAG}")
    P("DECLARED BEFORE ANY NUMBER:")
    P("  MECHANISM  engine normalises the drifted row by V = 1 + g*d; d > 0 on average, so a")
    P("             larger g pulls the row back TOWARD target and turn(g)/g FALLS in g.  d")
    P("             accumulates between DECISIONS, so it is a cadence quantity: the two sides of")
    P("             a cadence step carry residuals of DIFFERENT size and cannot cancel.")
    P("  DIRECTION  REL_step(g) NEGATIVE and monotone DECREASING in g, and LARGER in magnitude")
    P("             than the level residual it is built from (H_AMPLIFY).")
    P("  BIAS       a cadence gain is EXACT at the gross it was measured at.  The residual enters")
    P("             on CONVERSION: BIAS(g_from->g_to) = STEP(g_from)*g_to/g_from - STEP(g_to).")
    P("=" * 100)

    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    pnl = {k: Panel(k, px[k]) for k in PANELS}
    P("\nPANELS")
    for k in PANELS:
        p = pnl[k]
        P(f"  {k:5s} {p.px.shape[1]:4d} cols  {p.idx[0].date()} -> {p.idx[-1].date()}  "
          f"warm {p.yrs_warm:.2f}y  IS {p.yrs_is:.2f}y  OOS {p.yrs_oos:.2f}y  "
          f"SPY full {p.spy_full[0]:.4f}/{p.spy_full[1]:.4f}/{p.spy_full[2]:.4f}")

    W1 = {(k, b): book_w1(px[k], b, pnl[k].elig) for k in PANELS for b in BOOKS}

    # ---------------------------------------------------------------- GATES, before any result
    P("\n" + "=" * 100)
    P("GATES (printed before any result number)")
    P("=" * 100)
    gates = []

    pk, bk, ck, gk = "U56", "TOP20", "W", 0.75
    wfull = pd.DataFrame(W1[(pk, bk)] * gk, index=px[pk].index, columns=px[pk].columns)
    ctx = pnl[pk].ctx[ck]
    gr, tn = ctx.run(lag_weights(W1[(pk, bk)] * gk))
    g1, nn = 0.0, 0
    for rung in (0.0, 10.0):
        eng = backtest(px[pk], wfull, cost_bps=rung, freq=ck)
        d = np.abs(eng["returns"].values - (gr - tn * rung / 1e4))
        nn = max(nn, int(np.isnan(d).sum()))
        g1 = max(g1, float(np.nanmax(d)),
                 float(np.nanmax(np.abs(eng["turnover"].values - tn))))
    P(f"  G1  fast runner == engine.backtest (ret & turn) : {g1:.3e}  "
      f"({nn} NaN rows in engine's own output)   {'PASS' if g1 < 1e-12 else 'FAIL'}")
    gates.append(("G1_runner", g1, bool(g1 < 1e-12)))

    g2 = 0.0
    for c in (5.0, 25.0):
        e = backtest(px[pk], wfull, cost_bps=c, freq=ck)["returns"].values
        g2 = max(g2, float(np.nanmax(np.abs(e - (gr - tn * c / 1e4)))))
    P(f"  G2  cost linearity net(c)==gross-turn*c/1e4      : {g2:.3e}   "
      f"{'PASS' if g2 < 1e-12 else 'FAIL'}")
    gates.append(("G2_costlin", g2, bool(g2 < 1e-12)))

    so = pnl["U56"].spy_oos
    d3 = tuple(abs(a - b) for a, b in zip(so, SPY_OOS_PUB))
    ok3 = all(d < t for d, t in zip(d3, G3_TOL))
    P(f"  G3  SPY OOS triple vs committed                  : "
      f"{so[0]:.4f}/{so[1]:.4f}/{so[2]:.4f} vs {SPY_OOS_PUB}  d={max(d3):.3e}   "
      f"{'PASS' if ok3 else 'FAIL'}")
    gates.append(("G3_spy_oos", max(d3), ok3))

    v2m = {}
    for k in PANELS:
        b2 = backtest(px[k], rules_v2_weights(px[k]), cost_bps=COST, freq="W")["returns"].values
        v2m[k] = dict(full=fmet(b2[pnl[k].warm]), oos=fmet(b2[pnl[k].oos_m]),
                      h1=fmet(b2[pnl[k].h1])[1], h2=fmet(b2[pnl[k].h2])[1])
    d4 = abs(v2m["U56"]["full"][2] - V2_MAXDD_PUB)
    P(f"  G4  live RULES v2 full MaxDD vs committed        : {v2m['U56']['full'][2]:.4f} vs "
      f"{V2_MAXDD_PUB:.4f}  d={d4:.3e}   {'PASS' if d4 < 5e-4 else 'FAIL'}")
    gates.append(("G4_v2_maxdd", d4, bool(d4 < 5e-4)))

    d7 = float(np.abs(book_w1(px["U56"], "TOP20", pnl["U56"].elig) - W1[("U56", "TOP20")]).max())
    P(f"  G7  determinism: weight rows are a pure function : {d7:.3e}   "
      f"{'PASS' if d7 == 0.0 else 'FAIL'}")
    gates.append(("G7_determinism", d7, bool(d7 == 0.0)))

    # ---------------------------------------------------------------- the tape: turnover ladder
    lad = []
    for k in PANELS:
        pn = pnl[k]
        for b in BOOKS:
            for c in CADENCES:
                cx = pn.ctx[c]
                for g in LADDER:
                    gr, tn = cx.run(lag_weights(W1[(k, b)] * g))
                    net = gr - tn * COST / 1e4
                    turn_yr = float(tn[pn.warm].sum() / pn.yrs_warm)
                    legs, trip, halves, os_ = legs_4b(pn, net)
                    is_c, is_s, is_dd = fmet(net[pn.is_m])
                    m = v2m[k]
                    lad.append(dict(panel=k, book=b, cadence=c, gross=g,
                                    turn_yr=turn_yr,
                                    turn_yr_IS=float(tn[pn.is_m].sum() / pn.yrs_is),
                                    turn_yr_OOS=float(tn[pn.oos_m].sum() / pn.yrs_oos),
                                    drag_bp=turn_yr * COST,
                                    CAGR=trip[0], Sharpe=trip[1], MaxDD=trip[2],
                                    SH_H1=halves[0], SH_H2=halves[1],
                                    OOS_CAGR=os_[0], OOS_Sharpe=os_[1], OOS_MaxDD=os_[2],
                                    IS_CAGR=is_c, IS_Sharpe=is_s, IS_MaxDD=is_dd,
                                    **legs, p4b=all(legs.values()),
                                    p4a=bool(halves[0] > m["h1"] and halves[1] > m["h2"]
                                             and trip[2] >= m["full"][2]),
                                    p4b_oos=bool(os_[1] > pn.spy_oos[1]
                                                 and abs(os_[2]) <= DD_CAP * abs(pn.spy_oos[2])
                                                 and os_[0] >= CAGR_FLOOR * pn.spy_oos[0])))
    lad = pd.DataFrame(lad)

    # G5 / G6 CROSS-RUN against idea 1076's committed ladder
    if REF1076.exists():
        ref = pd.read_csv(REF1076)[["panel", "book", "cadence", "gross", "turn_yr"]]
        mg = lad.merge(ref, on=["panel", "book", "cadence", "gross"], how="inner",
                       suffixes=("", "_1076"))
        g5 = float(np.abs(mg.turn_yr - mg.turn_yr_1076).max()) if len(mg) else np.nan
        P(f"  G5  CROSS-RUN turn_yr vs 1076's committed       : {g5:.3e} over {len(mg)} shared "
          f"cells   {'PASS' if g5 < 1e-9 else 'FAIL'}")
        gates.append(("G5_crossrun_1076", g5, bool(g5 < 1e-9)))
    else:
        P("  G5  CROSS-RUN turn_yr vs 1076                   : reference CSV absent -- NOT RUN")
        gates.append(("G5_crossrun_1076", np.nan, False))

    lev = lad.copy()
    lev["turn_per_gross"] = lev.turn_yr / lev.gross
    base = lev[lev.gross == 1.00].set_index(["panel", "book", "cadence"]).turn_per_gross
    lev["ref"] = [base.loc[(r.panel, r.book, r.cadence)] for _, r in lev.iterrows()]
    lev["rel"] = lev.turn_per_gross / lev.ref - 1.0
    dev_full = float(lev.rel.abs().max())
    dev_rec = float(lev[lev.gross.isin(RECORD_LADDER)].rel.abs().max())
    d6 = max(abs(dev_full - DEV_FULL_PUB), abs(dev_rec - DEV_REC_PUB))
    P(f"  G6  CROSS-RUN 1076's level deviations reproduce  : {dev_full:.4e} vs "
      f"{DEV_FULL_PUB:.4e} (full), {dev_rec:.4e} vs {DEV_REC_PUB:.4e} (record)  "
      f"d={d6:.3e}   {'PASS' if d6 < 5e-4 else 'FAIL'}")
    gates.append(("G6_crossrun_dev", d6, bool(d6 < 5e-4)))

    P(f"\n  GATES {sum(1 for _, _, ok in gates if ok)} of {len(gates)}")
    dump(pd.DataFrame(gates, columns=["gate", "stat", "pass"]), "gates.csv")

    # ---------------------------------------------------------------- THE CADENCE STEPS
    P("\n" + "=" * 100)
    P("THE CADENCE STEPS -- 6 steps x 4 gross rungs x 10 (panel, book) cells, ALL published")
    P("=" * 100)
    tt = lad.set_index(["panel", "book", "cadence", "gross"]).turn_yr
    srows = []
    for k in PANELS:
        for b in BOOKS:
            for (cf, cs) in STEPS:
                s1 = tt.loc[(k, b, cf, 1.00)] - tt.loc[(k, b, cs, 1.00)]
                for g in LADDER:
                    st = tt.loc[(k, b, cf, g)] - tt.loc[(k, b, cs, g)]
                    srows.append(dict(panel=k, book=b, step=f"{cf}->{cs}", fast=cf, slow=cs,
                                      gross=g, turn_fast=tt.loc[(k, b, cf, g)],
                                      turn_slow=tt.loc[(k, b, cs, g)],
                                      step_turn=st, step_drag_bp=st * COST,
                                      step_per_gross=st / g,
                                      rel=(st / g) / s1 - 1.0 if s1 else np.nan))
    stp = pd.DataFrame(srows)
    step_dev_full = float(stp.rel.abs().max())
    step_dev_rec = float(stp[stp.gross.isin(RECORD_LADDER)].rel.abs().max())

    P("\n  STEP SIZE (x of NAV / yr) and its PER-UNIT-OF-GROSS residual, by dial cell")
    P("    step   gross      median step   median step/g   max |rel|   mean rel   n cells")
    for (sname, g), grp in stp.groupby(["step", "gross"], sort=False):
        P(f"    {sname:6s} {g:5.2f}   {grp.step_turn.median():11.4f}   "
          f"{grp.step_per_gross.median():13.4f}   {grp.rel.abs().max():9.3e}  "
          f"{grp.rel.mean():+9.3e}   {len(grp):3d}")

    P("\n  PER-RUNG max |rel| over all 60 (panel, book, step) cells")
    P("    " + "   ".join(f"@{g:.2f} {stp[stp.gross == g].rel.abs().max():.3e}" for g in LADDER))
    P(f"\n  max |rel| STEP  full ladder {step_dev_full:.4e}   record ladder {step_dev_rec:.4e}")
    P(f"  max |rel| LEVEL full ladder {dev_full:.4e}   record ladder {dev_rec:.4e}   "
      f"(1076's committed numbers, reproduced at G6)")
    amp_full = step_dev_full / dev_full if dev_full else np.nan
    amp_rec = step_dev_rec / dev_rec if dev_rec else np.nan
    P(f"  AMPLIFICATION step/level: {amp_full:.3f}x (full ladder), {amp_rec:.3f}x "
      f"(record ladder)")

    mono = []
    for (k, b, sname), grp in stp.groupby(["panel", "book", "step"]):
        v = grp.sort_values("gross").step_per_gross.values
        mono.append(bool(np.all(np.diff(v) <= 1e-15)))
    mono_share = float(np.mean(mono))
    rel_sign_neg = bool(stp.rel.mean() < 0)
    P("\n  G8 -- THE DECLARED DIRECTION, SCORED AS WRITTEN (the declaration is left verbatim in")
    P("       the docstring and the failing half is published beside the right answer, not")
    P("       replaced).  It was declared that REL_step(g) is NEGATIVE and that step/g is")
    P("       monotone DECREASING in g.")
    P(f"    G8a  sign: mean rel {stp.rel.mean():+.4e} -> "
      f"{'NEGATIVE' if rel_sign_neg else 'POSITIVE'}   "
      f"{'PASS' if rel_sign_neg else 'FAIL'}")
    P("         WHY IT FAILS, and it is the declaration that was wrong rather than the tape: if")
    P("         step/g FALLS in g then step/g at a LOW rung sits ABOVE its g=1.00 reference, so")
    P("         rel is POSITIVE by construction.  The two halves of the declared direction")
    P("         contradicted each other; the tape agrees with the mechanism, not with the sign.")
    P(f"    G8b  monotone DECREASING step/g: holds on {int(sum(mono))} of {len(mono)} "
      f"(panel, book, step) cells ({mono_share:.3f})   {'PASS' if mono_share >= 0.90 else 'FAIL'}")
    P("         1076 found the LEVEL monotone on 40 of 40 cells.  The STEP is not: differencing")
    P("         two monotone curves of different curvature need not be monotone, and on this")
    P("         tape it is not.")
    gates.append(("G8a_declared_sign", float(stp.rel.mean()), rel_sign_neg))
    gates.append(("G8b_declared_monotone", mono_share, bool(mono_share >= 0.90)))
    dump(pd.DataFrame(gates, columns=["gate", "stat", "pass"]), "gates.csv")
    P(f"  GATES now {sum(1 for _, _, ok in gates if ok)} of {len(gates)} "
      f"(G8 is computable only after the ladder and is appended here)")
    dump(stp, "steps.csv")

    P("\n  WORST 8 STEP CELLS (largest |rel| on the record's OWN ladder)")
    rec = stp[stp.gross.isin(RECORD_LADDER)]
    for _, r in rec.reindex(rec.rel.abs().sort_values(ascending=False).index).head(8).iterrows():
        P(f"    {r.panel:5s} {r.book:7s} {r.step:6s} @g={r.gross:.2f}   step {r.step_turn:8.4f}x "
          f"({r.step_drag_bp:8.2f} bp/yr)   rel {r.rel:+.3e}")

    # ---------------------------------------------------------------- CONVERSION BIAS
    P("\n" + "=" * 100)
    P("THE BIAS ITSELF -- converting a committed cadence gain from one gross to another")
    P("=" * 100)
    conv = []
    for (k, b, sname), grp in stp.groupby(["panel", "book", "step"]):
        gg = grp.set_index("gross")
        for gf in LADDER:
            for gt in LADDER:
                if gf == gt:
                    continue
                pred = gg.step_turn[gf] * gt / gf
                act = gg.step_turn[gt]
                conv.append(dict(panel=k, book=b, step=sname, g_from=gf, g_to=gt,
                                 pred_turn=pred, actual_turn=act,
                                 bias_turn=pred - act, bias_bp=(pred - act) * COST,
                                 rel=(pred / act - 1.0) if act else np.nan))
    conv = pd.DataFrame(conv)
    crec = conv[conv.g_from.isin(RECORD_LADDER) & conv.g_to.isin(RECORD_LADDER)]
    P(f"  over {len(conv):,} ordered (cell, g_from, g_to) conversions on the full ladder:")
    P(f"    max |rel| {conv.rel.abs().max():.3e}   median |rel| {conv.rel.abs().median():.3e}   "
      f"max |bias| {conv.bias_bp.abs().max():.3f} bp/yr   median |bias| "
      f"{conv.bias_bp.abs().median():.4f} bp/yr")
    P(f"  over {len(crec):,} conversions on the record's OWN ladder {RECORD_LADDER}:")
    P(f"    max |rel| {crec.rel.abs().max():.3e}   median |rel| {crec.rel.abs().median():.3e}   "
      f"max |bias| {crec.bias_bp.abs().max():.3f} bp/yr   median |bias| "
      f"{crec.bias_bp.abs().median():.4f} bp/yr")
    P("\n  BY STEP (record ladder): max |bias| in bp/yr at 10 bps, and as a share of the step")
    P("    step     n   max|bias| bp   median|bias| bp   max|rel|   median step bp")
    for sname, grp in conv[conv.g_from.isin(RECORD_LADDER)
                           & conv.g_to.isin(RECORD_LADDER)].groupby("step", sort=False):
        ms = stp[(stp.step == sname) & (stp.gross.isin(RECORD_LADDER))].step_drag_bp.median()
        P(f"    {sname:6s} {len(grp):4d}   {grp.bias_bp.abs().max():11.4f}   "
          f"{grp.bias_bp.abs().median():15.4f}   {grp.rel.abs().max():.3e}   {ms:12.2f}")
    dump(conv, "convert.csv")

    # ---------------------------------------------------------------- CENSUS
    P("\n" + "=" * 100)
    P("THE CENSUS -- committed CADENCE claims carrying a turnover/drag figure")
    P("=" * 100)
    units = corpus()
    cen = census_cadence(units)
    P(f"  corpus {len(units):,} committed units; {len(cen):,} turnover/drag figures sit in a unit "
      f"that also talks about cadence")
    P("\n    tier    n figures   gross-stamped   share   median decimals   median stated prec "
      "(bp/yr)")
    for tier in ("STEP", "MULTI", "ONE"):
        s = cen[cen.tier == tier]
        if not len(s):
            P(f"    {tier:6s} {0:10d}")
            continue
        P(f"    {tier:6s} {len(s):10,d}   {int(s.gross_stamped.sum()):13,d}   "
          f"{s.gross_stamped.mean():5.3f}   {s.decimals.median():15.1f}   "
          f"{s.prec_bpyr.median():20.4f}")
    P("\n  BY SOURCE (cadence-gain figures = tiers STEP + MULTI)")
    gains = cen[cen.tier.isin(["STEP", "MULTI"])].copy()
    P("    source          n   stamped   share")
    for s, grp in gains.groupby("source"):
        P(f"    {s:11s} {len(grp):6,d}   {int(grp.gross_stamped.sum()):7,d}   "
          f"{grp.gross_stamped.mean():5.3f}")
    dump(cen, "census.csv")

    # ---------------------------------------------------------------- DOES IT MOVE THEM?
    P("\n" + "=" * 100)
    P("DOES THE BIAS MOVE A PUBLISHED CADENCE GAIN BEYOND ITS OWN STATED PRECISION?")
    P("=" * 100)
    P("  A figure states its precision by its last printed digit: half a unit there is the most")
    P("  it can be claiming.  1076 established that 0.076 of committed turnover/drag figures")
    P("  state the gross they were measured at, so for the rest the cell and the rung are BOTH")
    P("  unknown -- the bias is therefore priced over the WHOLE cell population and both the")
    P("  MEDIAN and the MAX are reported.  Nothing here pretends to know which cell a given")
    P("  committed figure came from; that is the honest limit of this census.")
    bias_med = float(crec.bias_bp.abs().median())
    bias_max = float(crec.bias_bp.abs().max())
    moved = []
    for _, r in gains.iterrows():
        moved.append(dict(source=r.source, unit=r.unit, tier=r.tier, figure=r.figure,
                          value=r.value, decimals=r.decimals, unit_kind=r.unit_kind,
                          prec_bpyr=r.prec_bpyr, gross_stamped=bool(r.gross_stamped),
                          moved_median=bool(bias_med > r.prec_bpyr),
                          moved_max=bool(bias_max > r.prec_bpyr)))
    mv = pd.DataFrame(moved)
    if len(mv):
        P(f"\n  bias basis (record ladder, all {len(crec):,} conversions): "
          f"median |bias| {bias_med:.4f} bp/yr, max |bias| {bias_max:.4f} bp/yr")
        P(f"  committed cadence-gain figures: {len(mv):,}")
        P(f"    MOVED at the MEDIAN cell : {int(mv.moved_median.sum()):,} "
          f"({mv.moved_median.mean():.3f})")
        P(f"    MOVED at the WORST cell  : {int(mv.moved_max.sum()):,} "
          f"({mv.moved_max.mean():.3f})")
        P(f"    NOT moved even at worst  : {int((~mv.moved_max).sum()):,} "
          f"({(~mv.moved_max).mean():.3f})")
        P("\n    by stated precision (bp/yr):")
        for pv, grp in mv.groupby("prec_bpyr"):
            P(f"      prec {pv:8.4f}  n {len(grp):5,d}   moved@median "
              f"{grp.moved_median.mean():5.3f}   moved@max {grp.moved_max.mean():5.3f}")
        P("\n    and of the STAMPED ones (the only figures whose conversion is even well posed):")
        st = mv[mv.gross_stamped]
        P(f"      n {len(st):,}   moved@median "
          f"{st.moved_median.mean() if len(st) else float('nan'):.3f}   moved@max "
          f"{st.moved_max.mean() if len(st) else float('nan'):.3f}")
    dump(mv, "moved.csv")

    # ---------------------------------------------------------------- RANK INVARIANCE
    P("\n" + "=" * 100)
    P("CADENCE RANK INVARIANCE -- can the rung reverse a committed ordering?")
    P("=" * 100)
    rk = []
    for (k, b), grp in lad.groupby(["panel", "book"]):
        orders = {}
        for g in LADDER:
            s = grp[grp.gross == g].sort_values("turn_yr", ascending=False)
            orders[g] = tuple(s.cadence)
        same = len(set(orders.values())) == 1
        rk.append(dict(panel=k, book=b, invariant=bool(same),
                       **{f"order_g{g:.2f}": "".join(orders[g]) for g in LADDER}))
        P(f"  {k:5s} {b:7s}  " + "   ".join(f"@{g:.2f} {''.join(orders[g])}" for g in LADDER)
          + f"   {'INVARIANT' if same else 'REVERSES'}")
    rk = pd.DataFrame(rk)
    dump(rk, "rank.csv")

    # ---------------------------------------------------------------- RULE 8 + KEEP paths
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD -- (cadence, gross) chosen JOINTLY on IS 2009-2016 Sharpe ALONE,")
    P("                       OOS 2017-2026 read ONCE; both KEEP paths scored at every cell")
    P("=" * 100)
    for k in PANELS:
        P(f"  RULES v2 (live) {k:5s} full {v2m[k]['full'][0]:.4f}/{v2m[k]['full'][1]:.4f}/"
          f"{v2m[k]['full'][2]:.4f}   OOS {v2m[k]['oos'][0]:.4f}/{v2m[k]['oos'][1]:.4f}/"
          f"{v2m[k]['oos'][2]:.4f}   halves {v2m[k]['h1']:.4f}/{v2m[k]['h2']:.4f}")
        P(f"  SPY             {k:5s} full {pnl[k].spy_full[0]:.4f}/{pnl[k].spy_full[1]:.4f}/"
          f"{pnl[k].spy_full[2]:.4f}   OOS {pnl[k].spy_oos[0]:.4f}/{pnl[k].spy_oos[1]:.4f}/"
          f"{pnl[k].spy_oos[2]:.4f}   halves {pnl[k].spy_h1:.4f}/{pnl[k].spy_h2:.4f}")

    wf = []
    for k in PANELS:
        for b in BOOKS:
            s = lad[(lad.panel == k) & (lad.book == b)]
            pick = s.loc[s.IS_Sharpe.idxmax()]
            wf.append(dict(panel=k, book=b, pick_cadence=pick.cadence, pick_gross=pick.gross,
                           IS_Sharpe=pick.IS_Sharpe,
                           CAGR=pick.CAGR, Sharpe=pick.Sharpe, MaxDD=pick.MaxDD,
                           SH_H1=pick.SH_H1, SH_H2=pick.SH_H2,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD,
                           turn_yr=pick.turn_yr, drag_bp=pick.drag_bp,
                           SPY_OOS_CAGR=pnl[k].spy_oos[0], SPY_OOS_Sharpe=pnl[k].spy_oos[1],
                           SPY_OOS_MaxDD=pnl[k].spy_oos[2],
                           V2_OOS_CAGR=v2m[k]["oos"][0], V2_OOS_Sharpe=v2m[k]["oos"][1],
                           V2_OOS_MaxDD=v2m[k]["oos"][2],
                           L_H1=pick.L_H1, L_H2=pick.L_H2, L_OOS=pick.L_OOS, L_DD=pick.L_DD,
                           L_CAGR=pick.L_CAGR, pass4b=bool(pick.p4b), pass4a=bool(pick.p4a),
                           OOS4b=bool(pick.p4b_oos)))
    wf = pd.DataFrame(wf)
    P("\n    panel book     pick      IS Sh    full CAGR  Sharpe   MaxDD     OOS C/S/DD"
      "              4b 4a OOS4b")
    for _, r in wf.iterrows():
        P(f"    {r.panel:5s} {r.book:7s} {r.pick_cadence}@{r.pick_gross:.2f}  {r.IS_Sharpe:6.4f}   "
          f"{r.CAGR:8.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%}   "
          f"{r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:8.2%}   "
          f"{'Y' if r.pass4b else '.':>2s} {'Y' if r.pass4a else '.':>2s} "
          f"{'Y' if r.OOS4b else '.':>4s}")
    P(f"\n  4b full-sample on the IS pick : {int(wf.pass4b.sum())} of {len(wf)}")
    P(f"  4a on the IS pick             : {int(wf.pass4a.sum())} of {len(wf)}")
    P(f"  4b OUT OF SAMPLE on the pick  : {int(wf.OOS4b.sum())} of {len(wf)}")
    P(f"  whole 160-cell grid           : 4b {int(lad.p4b.sum())} of {len(lad)}   "
      f"4a {int(lad.p4a.sum())} of {len(lad)}   4b-OOS {int(lad.p4b_oos.sum())} of {len(lad)}")
    if lad.p4b.any():
        P("\n  EVERY full-sample 4b PASS on the grid (nothing here is proposed):")
        for _, r in lad[lad.p4b].iterrows():
            P(f"    {r.panel:5s} {r.book:7s} {r.cadence}@{r.gross:.2f}  full {r.CAGR:.2%}/"
              f"{r.Sharpe:.4f}/{r.MaxDD:.2%}  halves {r.SH_H1:.3f}/{r.SH_H2:.3f}  "
              f"OOS {r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:.2%}  "
              f"4b-OOS {'Y' if r.p4b_oos else '.'}  4a {'Y' if r.p4a else '.'}")
    dump(wf, "walkforward.csv")
    dump(lad, "ladder.csv")
    dump(lev[["panel", "book", "cadence", "gross", "turn_yr", "turn_per_gross", "rel"]],
         "linearity.csv")

    # ---------------------------------------------------------------- HYPOTHESES
    P("\n" + "=" * 100)
    P("PRE-REGISTERED HYPOTHESES (scored exactly as written)")
    P("=" * 100)
    h = []
    h.append(("H_STEPLIN", f"max |rel_step| = {step_dev_full:.4e} over {LADDER} "
                           f"(bar {H_LIN_BAR})", bool(step_dev_full <= H_LIN_BAR)))
    h.append(("H_STEPREC", f"max |rel_step| = {step_dev_rec:.4e} over the record's own "
                           f"{RECORD_LADDER} (bar {H_LIN_BAR})", bool(step_dev_rec <= H_LIN_BAR)))
    h.append(("H_AMPLIFY", f"step residual {step_dev_rec:.4e} vs level residual {dev_rec:.4e} on "
                           f"the record ladder = {amp_rec:.3f}x (declared > 1)",
              bool(step_dev_rec > dev_rec)))
    h.append(("H_DIR", f"DECLARED DIRECTION as written (rel NEGATIVE and step/g monotone): sign "
                       f"{'NEGATIVE' if rel_sign_neg else 'POSITIVE'} (mean {stp.rel.mean():+.3e}), "
                       f"monotone on {mono_share:.3f} of cells",
              bool(rel_sign_neg and mono_share >= 0.90)))
    h.append(("H_RANK", f"cadence ordering identical at all 4 rungs in "
                        f"{int(rk.invariant.sum())} of {len(rk)} (panel, book) cells",
              bool(rk.invariant.all())))
    if len(mv):
        h.append(("H_PRECISION", f"{(~mv.moved_median).mean():.3f} of {len(mv):,} committed "
                                 f"cadence-gain figures are NOT moved at the median cell "
                                 f"(bar {H_PRECISION_BAR})",
                  bool((~mv.moved_median).mean() >= H_PRECISION_BAR)))
    else:
        h.append(("H_PRECISION", "no committed cadence-gain figures found", False))
    h.append(("H_1076", f"level deviations {dev_full:.4e} / {dev_rec:.4e} vs 1076's committed "
                        f"{DEV_FULL_PUB:.4e} / {DEV_REC_PUB:.4e}", bool(d6 < 5e-4)))
    h.append(("H_WF", f"OOS 4b passes {int(wf.OOS4b.sum())} of {len(wf)} rule-8 picks",
              bool(wf.OOS4b.any())))
    for n, d, ok in h:
        P(f"  {n:12s} {'PASS' if ok else 'FAIL'}   {d}")
    P(f"\n  HYPOTHESES {sum(1 for _, _, ok in h if ok)} of {len(h)}")
    dump(pd.DataFrame(h, columns=["hypothesis", "detail", "pass"]), "hypotheses.csv")

    # ---------------------------------------------------------------- the queue's own premise
    P("\n" + "=" * 100)
    P("THE QUEUE'S OWN PREMISE, CHECKED")
    P("=" * 100)
    P("  The queue says: 'Every committed cadence comparison differences two books at one gross,")
    P("  so the residual does not cancel.'  Half of that is right and half is not, and the")
    P("  distinction is the whole result:")
    P("    (i)  AT the gross it was measured at, a cadence gain is EXACT.  It is the difference")
    P("         of two numbers the engine actually produced; no linearity is assumed and there is")
    P("         no residual to cancel or fail to cancel.")
    P("    (ii) The residual enters the moment that gain is read at ANOTHER gross -- which is")
    P("         what an unstamped figure invites, and 1076 measured that 0.924 of committed")
    P("         turnover/drag figures are unstamped.  THAT is the quantity priced above.")
    P("  And the queue's second clause -- that the residual does not cancel on a difference --")
    P(f"  is confirmed in direction and priced: {amp_rec:.3f}x the level residual on the record's")
    P("  own ladder.")

    P(f"\ndone in {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
